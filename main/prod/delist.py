import requests
from datetime import datetime
from time import sleep
import re
from config.config import ACCOUNT_ID_DELIST
from common.domain.delist_announcement import DelistAnnouncement
from common.dao.delist_announcement_dao import get_delist_announcement_by_coin, insert_delist_announcement
from common.domain.account_balance import AccountBalance
from common.dao.account_balance_dao import get_account_balance, update_account_balance
from common.enums import Account_Operation_Type, Side_Type, Strategy_Operation_Type
from common.util import get_pairs_precision, get_pairs_price_precision
from prod.binance import Binance
from prod import delist_logger as logger

BASE_STABLE_COIN = 'USDT'
BALANCE_SAFE_PERCENTAGE = 0.8 # 80% of the available balance will be used for opening positions

class Delist():
    def __init__(self, strategy, exchange_session):
        self.strategy = strategy # We'll have only one strategy for delist
        self.exchange_session = exchange_session
        self.available_balance = self._update_available_balance()
        self.setup = None # It's a 

    def get_delisting_coins(self):
        """
        Scrape Binance announcements to find new delisting announcements.
        If a new announcement is found, it is added to the database and the coins are extracted.
        :return: A list of coins to be delisted, or None if no new announcements are found.
        """
        for announcement in _get_binance_announcements():
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
        account_balance_dao.update_account_balance(ACCOUNT_ID_DELIST, account_balance)
        return account_balance

    
    def _get_available_balance(self):
        account_balance: AccountBalance = get_account_balance(ACCOUNT_ID_DELIST)
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
            sleep(3600)
            self.handle_opened_trades()

        # while there are no new delisting coins, sleep for 1 minute and check again.
        # if there are new delisting coins, we will get them and open trades for them.
        delist_coins = self.get_delisting_coins()
        while not delist_coins:
            sleep(60)
            delist_coins = self.get_delisting_coins()

        # If we reach here, it means there are new delisting coins to handle.
        self.handle_new_trades(delist_coins)
        
    def _has_open_trades(self):
        opened_trades = trade_dao.get_open_trades_by_operation_type(Strategy_Operation_Type.DELIST.value)
        return len(opened_trades) > 0

    def handle_new_trades(self, delist_coins):
        self.pairs_precision = get_pairs_precision(delist_coins)
        self.get_pairs_price_precision = get_pairs_price_precision(delist_coins)
        self.setup.order_value = self._define_open_order_value(delist_coins)
        for coin in delist_coins:
            pair = f"{coin}{BASE_STABLE_COIN}"
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
                if manager.try_open_position():
                    available_orders -= 1
                    self.current_balance = self._get_current_balance()
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

        # getting trend candle dataset from binance
        trend_data = CandleData(
            pair, strategy.trend_interval, start_date, "trend")
        trend_data.populate_data(round(time.time()*1000))

        # adding strategy indicators to trend dataset
        trend_dataset = Dataset(trend_data.candle_df, strategy)
        trend_indicators_list = trend_dataset.add_indicators_to_candle_dataset(
            "trend")

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
        