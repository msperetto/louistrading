import requests
from datetime import datetime
import re
import time
from config.config import ACCOUNT_ID_DELIST, NEGOCIATION_ENV, USE_TEST_ANNOUNCEMENTS, BASE_LOCAL_URL
from common.domain.delist_announcement import DelistAnnouncement
from common.dao.delist_announcement_dao import get_delist_announcement_by_coin, insert_delist_announcement
from common.dao.test_delist_announcement_dao import get_unprocessed_test_announcements, mark_announcement_processed
from common.domain.account_balance import AccountBalance
from common.dao import trade_dao, alert_dao, strategy_dao, account_balance_dao
from common.enums import Strategy_Operation_Type, Alert_Level, Environment_Type
from common.util import get_pairs_precision, get_pairs_price_precision
from prod.binance import Binance
from prod.dataset import Dataset
from prod.candle_data import CandleData
from common import management
from prod.strategy_manager import StrategyManager
from prod import delist_logger as logger
from prod import notify

BASE_STABLE_COIN = 'USDT'
BALANCE_SAFE_PERCENTAGE = 0.8 # 80% of the available balance will be used for opening positions

class Delist():
    def __init__(self, strategy, exchange_session):
        self.strategy = strategy # We'll have only one strategy for delist
        self.exchange_session = exchange_session
        self.margin_ratio = 2  # Assuming a margin ratio of 2 for simplicity
        self.available_balance = self._update_available_balance()
        self.setup = None # It's a 

    def get_delisting_coins(self):
        """
        Scrape Binance announcements to find new delisting announcements.
        If in TEST mode and USE_TEST_ANNOUNCEMENTS is True, uses fake announcements from database.
        If a new announcement is found, it is added to the database and the coins are extracted.
        :return: A list of coins to be delisted, or None if no new announcements are found.
        """
        # Check if we should use test announcements
        if NEGOCIATION_ENV == Environment_Type.TEST and USE_TEST_ANNOUNCEMENTS:
            return self._get_delisting_coins_from_test_data()
        else:
            return self._get_delisting_coins_from_binance()

    def _get_delisting_coins_from_test_data(self):
        """
        Get delisting coins from test announcements in the database.
        This method mirrors the production logic to test the exact same flow.
        :return: A list of coins to be delisted, or None if no new announcements are found.
        """
        logger.info("Using TEST mode - fetching announcements from database")
        
        try:
            test_announcements = get_unprocessed_test_announcements()
            
            for test_ann in test_announcements:
                title = test_ann.title
                logger.info(f"Processing test announcement: {title}")
                
                # Mirror production logic: check if title contains delist keyword
                if "Binance Will Delist" in title:
                    new_delist_coins = []
                    
                    # Extract date from title (same as production)
                    announcement_date = self._extract_date_from_title(title)
                    
                    # If date not found in title, use the stored announcement_date
                    if not announcement_date:
                        announcement_date = test_ann.announcement_date
                        logger.info(f"Date not found in title, using stored date: {announcement_date}")
                    
                    # Extract coins from title (same as production)
                    coins = self._extract_tickers_from_title(title)
                    
                    # If extraction fails, use the stored coins list
                    if not coins:
                        coins = test_ann.coins
                        logger.info(f"Coins not extracted from title, using stored coins: {coins}")
                    
                    # Process each coin (same as production)
                    for coin in coins:
                        if self._is_new_announcement(coin):
                            ticker = f"{coin}{BASE_STABLE_COIN}"
                            if self.is_ticker_in_futures(ticker):
                                logger.info(f"New delist announcement found for coin: {coin} - Announcement date: {announcement_date}")
                                new_delist_coins.append(coin)
                                insert_delist_announcement(announcement_date, coin)
                    
                    # Mark test announcement as processed
                    mark_announcement_processed(test_ann.id)
                    logger.info(f"Test announcement {test_ann.id} marked as processed")
                    
                    if new_delist_coins:
                        return new_delist_coins
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing test announcements: {e}")
            return None

    def _get_delisting_coins_from_binance(self):
        """
        Get delisting coins from real Binance announcements.
        :return: A list of coins to be delisted, or None if no new announcements are found.
        """
        logger.info("Using PRODUCTION mode - fetching announcements from Binance")
        
        for announcement in self._get_binance_announcements():
            title = announcement.get('title')

            if "Binance Will Delist" in title:
                new_delist_coins = [] # List to hold newly found delist coins
                # Extract the date in the format 'YYYY-MM-DD in the title'
                announcement_date = self._extract_date_from_title(title)

                coins = self._extract_tickers_from_title(title)

                for coin in coins:
                    if self._is_new_announcement(coin):
                        ticker = f"{coin}{BASE_STABLE_COIN}"
                        if self.is_ticker_in_futures(ticker):
                            logger.info(f"New delist announcement found for coin: {coin} - Announcement date: {announcement_date}")
                            new_delist_coins.append(coin)
                            insert_delist_announcement(announcement_date, coin)
                return new_delist_coins

        return None

    def _extract_date_from_title(self, title):
        """
        Extract the announcement date from the title string.
        :param title: The announcement title string.
        :return: The extracted date in 'YYYY-MM-DD' format, or None if not found.
        """
        match = re.search(r'(\d{4}-\d{2}-\d{2})', title)
        if match:
            return match.group(1)
        return None
        

    def _get_binance_announcements(self):
        """
        Fetch the latest announcements from Binance and parse them.
        :return: A list of dictionaries with all 1st page delist announcements.
            (fields: id, code, title, type, releaseDate(in miliseconds))
        """
        announcements = Binance().get_delist_announcements()
        return announcements

    def _extract_tickers_from_title(self, title):
        """
        Extract tickers from the announcement title.
        :param title: The announcement title string.
        :return: A list of extracted ticker symbols.
        """
        # Extract tickers (between "Binance Will Delist" and "on YYYY-MM-DD")
        match = re.search(r"Binance Will Delist (.+?) on \d{4}-\d{2}-\d{2}", title)
        if match:
            tickers_text = match.group(1)  # Get the part with tickers
            tickers = re.findall(r"\b[A-Z]{2,}\b", tickers_text)  # Extract tickers
            return tickers

    def _get_all_futures_symbols(self):
        return Binance().get_all_symbols()
    
    def _is_new_announcement(self, coin):
        """
        Check if an announcement coin has already been utilized (exists in DB).
        :param coin: The announcement coin to check.
        :return: True if the announcement coin exists in the database, False otherwise.
        """
        announcement = get_delist_announcement_by_coin(coin)
        if announcement:
            return False
        return True

    def is_ticker_in_futures(self, ticker):
        """
        Check if a ticker is being traded in Binance Futures.
        :param ticker: The ticker symbol to check (e.g., 'BTCUSDT').
        :return: True if the ticker is traded in Binance Futures, False otherwise.
        """
        return ticker in self._get_all_futures_symbols()

    def _update_available_balance(self):
        account_balance = float(Binance().get_account_info(self.exchange_session.e_id, self.exchange_session.e_sk)["availableBalance"])
        account_balance_dao.update_account_balance(ACCOUNT_ID_DELIST, account_balance, self.margin_ratio)
        return account_balance

    
    def _get_available_balance(self):
        account_balance: AccountBalance = account_balance_dao.get_account_balance(ACCOUNT_ID_DELIST)
        if account_balance:
            return account_balance.account_balance
        return 0.0


    def run(self):
        """
        Main method to be run in a while true loop.
        Will check for new delisting announcements and enter trade when found.
        Also will handle opened trades.
        """
        # First check if there is any opened trade, if so, handle the closing of the trade.
        while self._has_open_trades():
            #TODO: think if make sense to create a _should_run_strategy method for delist strategy.
            # Similar to what we do in tradingBot, so it runs depending on the candle interval.
            # sleeps for 1 hour and try to handle opened trades again.
            time.sleep(3600)
            self.handle_opened_trades()

        # while there are no new delisting coins, sleep for 1 minute and check again.
        # if there are new delisting coins, we will get them and open trades for them.
        delist_coins = self.get_delisting_coins()
        while not delist_coins:
            time.sleep(60)
            delist_coins = self.get_delisting_coins()

        # If we reach here, it means there are new delisting coins to handle.
        self.handle_new_trades(delist_coins)
        
    def _has_open_trades(self):
        opened_trades = trade_dao.get_open_trades_by_operation_type(Strategy_Operation_Type.DELIST.value)
        return len(opened_trades) > 0

    def handle_new_trades(self, delist_coins):
        # Build valid pairs (e.g., 'FORTHUSDT') for all coins that are in futures
        valid_pairs = [f"{coin}{BASE_STABLE_COIN}" for coin in delist_coins]

        self.pairs_precision = get_pairs_precision(valid_pairs)
        self.pairs_price_precision = get_pairs_price_precision(valid_pairs)
        self.setup.order_value = self._define_open_order_value(valid_pairs)

        binance = Binance()

        for pair in valid_pairs:
            coin = pair.replace(BASE_STABLE_COIN, '')
            final_dataset = self.create_combined_dataset(pair, self.strategy)
            manager = StrategyManager(
                    pair,
                    self.pairs_precision[pair],
                    self.pairs_price_precision[pair],
                    final_dataset,
                    self.exchange_session.e_id,
                    self.exchange_session.e_sk,
                    self.setup,
                    self.strategy
                )
            try:
                # In TEST mode, simulate the position instead of opening it
                if NEGOCIATION_ENV == Environment_Type.TEST:
                    # Calculate quantity based on order value and current price
                    current_price = float(binance.get_symbol_price(pair))
                    quantity = round(self.setup.order_value / current_price, self.pairs_precision[pair])
                    
                    # Get simulated position details from orderbook
                    position_details = binance.simulate_position_details(
                        pair, 
                        quantity, 
                        self.strategy.side
                    )
                    
                    # Log detailed information about what would be traded
                    logger.info("="*80)
                    logger.info("SIMULATED POSITION OPENING (TEST MODE)")
                    logger.info("="*80)
                    logger.info(f"Pair: {pair}")
                    logger.info(f"Coin: {coin}")
                    logger.info(f"Strategy: {self.strategy.name}")
                    logger.info(f"Side: {position_details.get('side', 'N/A')}")
                    logger.info(f"Order Type: {position_details.get('order_type', 'N/A')}")
                    logger.info(f"Quantity: {position_details.get('quantity', 'N/A')}")
                    logger.info(f"Estimated Entry Price: {position_details.get('estimated_price', 'N/A')}")
                    logger.info(f"Order Value (USDT): {self.setup.order_value}")
                    logger.info(f"Estimated Total Value: {position_details.get('estimated_total_value', 'N/A')}")
                    logger.info(f"Available Balance: {self.available_balance}")
                    logger.info(f"Orderbook Top 5 Bids: {position_details.get('orderbook_snapshot', {}).get('top_5_bids', [])}")
                    logger.info(f"Orderbook Top 5 Asks: {position_details.get('orderbook_snapshot', {}).get('top_5_asks', [])}")
                    
                    if 'error' in position_details:
                        logger.error(f"Error in simulation: {position_details['error']}")
                    else:
                        logger.info("Position would be opened successfully (simulated)")
                    
                    logger.info("="*80)
                    
                    # In test mode, we don't actually open the position
                    continue
                else:
                    # Production mode: actually open the position
                    if manager.try_open_position():
                        self.available_balance = self._update_available_balance()
                        # If the position was opened, then jump to the next pair.
                        continue
            except Exception as e:
                logger.error(f"An error occurred while trying to open position for pair {pair} with strategy {self.strategy}: {e}")
                alert_dao.insert_alert(
                    pair,
                    Alert_Level.ERROR,
                    True,
                    f"An error occurred while trying to open position for pair {pair} with strategy {self.strategy}: {e}"
                )
                # Notify the user about the error
                notify.send_message_alert(
                    f"An error occurred while trying to open position for pair {pair} with strategy {self.strategy}: {e}"
                )
                continue


    def handle_opened_trades(self):
        # Handle opened trades. Check if we is ready to sell.
        logger.debug(f"handle_opened_trades - begin")

        # get opened trades by the strategy operation type:
        opened_trades = trade_dao.get_open_trades_by_operation_type(Strategy_Operation_Type.DELIST.value)

        # TODO: What if an exception occurs in a specific trade?
        # We might want to continue processing the for loop and try to close the next trade. 
        for trade in opened_trades:
            try:
                strategyObject = strategy_dao.get_strategy_by_id(trade.strategy_id)
                strategyClassName = globals().get(strategyObject.name)
                #instantiate the strategy class:
                strategy = strategyClassName()


                logger.debug(f"handle_opened_trades - pair: {trade.pair}")
                logger.debug(f"current balance: {self.current_balance}")


                #TODO: check here if make sense to reuse the method from tradingbot,
                # or we will have some differences in delist strategy.
                final_dataset = self.create_combined_dataset(trade.pair, strategy)

                #logging for debugging
                logger.info(f"TRYING TO CLOSE POSITION - Pair: {trade.pair}")
                logger.debug(f"Pair: {trade.pair} - datetime: {datetime.now()} - final_dataset:\n{final_dataset}")

                manager = StrategyManager(
                    trade.pair,
                    self.pairs_precision[trade.pair],
                    self.pairs_price_precision[trade.pair],
                    final_dataset,
                    self.exchange_session.e_id,
                    self.exchange_session.e_sk,
                    self.setup,
                    strategy
                )
                if manager.try_close_position(strategy, trade.id):
                    self.available_balance = self._update_available_balance()

            except Exception as e:
                logger.error(f"An error occurred while trying to close position for trade {trade.id}: {e}")
                alert_dao.insert_alert(
                    trade.pair,
                    Alert_Level.ERROR,
                    True,
                    f"An error occurred while trying to close position for trade {trade.id}: {e}"
                )
                notify.send_message_alert(
                    f"An error occurred while trying to close position for trade {trade.id}: {e}"
                )
                continue


    def create_combined_dataset(self, pair, strategy):
        # calculating de date for the first candle of the dataset
        start_date = management.calc_start_date(strategy)

        # getting intraday candle dataset from binance
        intraday_data = CandleData(
            pair, strategy.intraday_interval, start_date, "intraday")
        intraday_data.populate_data(round(time.time()*1000))

        # adding strategy indicators to intraday dataset
        intraday_dataset = Dataset(intraday_data.candle_df, strategy)
        intraday_dataset.add_indicators_to_candle_dataset("intraday")

        # logging intraday dataset for debugging:
        logger.debug(f"Intraday dataset for {pair}:\n{intraday_dataset.dataset}")

        # getting trend candle dataset from binance
        trend_data = CandleData(
            pair, strategy.trend_interval, start_date, "trend")
        trend_data.populate_data(round(time.time()*1000))

        # adding strategy indicators to trend dataset
        trend_dataset = Dataset(trend_data.candle_df, strategy)

        trend_indicators_list = trend_dataset.add_indicators_to_candle_dataset("trend")

        #logging trend dataset for debugging:
        logger.debug(f"Trend dataset for {pair} after adding indicators:\n{trend_dataset.dataset}")

        # logging trend indicators list for debugging:
        logger.debug(f"Trend indicators list for {pair}: {trend_indicators_list}")

        #merging intraday and trend datasets in one final dataset
        return intraday_dataset.merge_dataframes(trend_dataset.dataset, *trend_indicators_list)

    def _define_open_order_value(self, coins: list):
        """
        Define the order value to be used when opening a new position.
        Based on a safe % margin of the available balance divided by the total number of coins
        :return: The order value to be used.
        """
        self.available_balance = self._get_available_balance()
        order_value = (self.available_balance * BALANCE_SAFE_PERCENTAGE) / len(coins)
        logger.info(f"Available balance: {self.available_balance}, Order value per coin: {order_value}")
        return order_value
