import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from prod.binance import Binance
from common.domain.delist_announcement import DelistAnnouncement
from common.dao.delist_announcement_dao import get_delist_announcement_by_coin, insert_delist_announcement

BASE_STABLE_COIN = 'USDT'

class Delist():
    def __init__(self):
        pass

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
