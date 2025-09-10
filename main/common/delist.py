import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from prod.binance import Binance
from common.domain.delist_announcement import DelistAnnouncement
from common.dao.delist_announcement_dao import get_delist_announcements, insert_delist_announcement

BASE_URL = "https://www.binance.com"
DELISTING_URL = "https://www.binance.com/en/support/announcement/list/161"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

BASE_STABLE_COIN = 'USDT'


class Delist():
    def __init__(self):
        pass

    def get_delisting_coins(self):
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
        response = requests.get(DELISTING_URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # geting all <a> tags
        return soup.find_all("a")

    def _extract_tickers_from_title(self, title):
        # Extract tickers (between "Binance Will Delist" and "on YYYY-MM-DD")
        match = re.search(r"Binance Will Delist (.+?) on \d{4}-\d{2}-\d{2}", title)
        if match:
            tickers_text = match.group(1)  # Get the part with tickers
            tickers = re.findall(r"\b[A-Z]{2,}\b", tickers_text)  # Extract tickers
            return tickers

    def _get_all_futures_symbols(self):
        return Binance().get_all_futures_symbols()
    
    def _check_utilized_announcement(self, announcement_date):
        existing_announcements = get_delist_announcements()
        for ann in existing_announcements:
            if ann.announcement_date == announcement_date:
                return True
        return False

    def check_ticker_in_futures(self, ticker):
        return ticker in self._get_all_futures_symbols()
