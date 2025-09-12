import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from prod.binance import Binance
from common.domain.delist_announcement import DelistAnnouncement
from common.dao.delist_announcement_dao import get_delist_announcements, insert_delist_announcement

BASE_STABLE_COIN = 'USDT'


class Delist():
    def __init__(self):
        pass

    def get_delisting_coins(self):
        """
        Scrape Binance announcements to find new delisting announcements.
        If a new announcement is found, it is added to the database and the tickers are extracted.
        :return: A list of tickers to be delisted, or None if no new announcements are found.
        """
        for announcement in get_binance_announcements():
            title = announcement.get_text(strip=True)
            link = announcement.get("href")

            if link and "Binance Will Delist" in title:
                # Get the next sibling element, which contain the date of the announcement
                announcement_date = announcement.find_next_sibling().get_text(strip=True)

                # Check if the announcement has been already utilized:
                if self._check_utilized_announcement(announcement_date):
                    continue

                # If the announcement is new, add it to table and extract the tickers:
                insert_delist_announcement(announcement_date)
                tickers = self._extract_tickers_from_title(title)
                if tickers:
                    return tickers
        return None

    def get_binance_announcements(self):
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
    
    def _check_utilized_announcement(self, announcement_date):
        """
        Check if an announcement date has already been utilized (exists in DB).
        :param announcement_date: The announcement date to check (format 'YYYY-MM-DD').
        :return: True if the announcement date exists in the database, False otherwise.
        """
        existing_announcements = get_delist_announcements()
        for ann in existing_announcements:
            if ann.announcement_date == announcement_date:
                return True
        return False

    def check_ticker_in_futures(self, ticker):
        """
        Check if a ticker is being traded in Binance Futures.
        :param ticker: The ticker symbol to check (e.g., 'BTCUSDT').
        :return: True if the ticker is traded in Binance Futures, False otherwise.
        """
        return ticker in self._get_all_futures_symbols()
