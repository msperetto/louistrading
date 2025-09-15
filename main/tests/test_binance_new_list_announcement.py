# Just testing new announcements for binance listings;
# The aim is to compare the time of the announcement is captured with the time
# the coin is actually listed.

from prod.binance import Binance
from datetime import datetime, timezone
from common.dao.list_announcement_dao import get_list_announcement_by_id, insert_list_announcement
from common.domain.list_announcement import ListAnnouncement
import re
import time

def _get_binance_announcements():
    """
    Fetch the latest announcements from Binance and parse them.
    :return: A list of dictionaries with all 1st page listing announcements.
        (fields: id, code, title, type, releaseDate(in miliseconds))
    """
    announcements = Binance().get_list_announcements()
    return announcements


def check_new_listing_announcements():
    """
    Scrape Binance announcements to find new listing announcements.
    If a new announcement is found, it is added to the database.
    :return: A list of new listing announcements, or None if no new announcements are found.
    """
    new_list_announcements = []
    for announcement in _get_binance_announcements():
        title = announcement.get('title')
        announcement_id = announcement.get('id')

        # Check if the announcement is already in the database
        existing_announcement = get_list_announcement_by_id(announcement_id)
        if existing_announcement is None:
            # If not, insert it into the database
            print(f"New listing announcement found: ID {announcement_id}, Title: {title}")
            captured_date = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            insert_list_announcement(announcement_id, title, captured_date)
            new_list_announcements.append(announcement)

    return new_list_announcements if new_list_announcements else None


if __name__ == "__main__":
    while True:
        new_announcements = check_new_listing_announcements()
        # Wait for a certain period before checking again (e.g., 1 hour)
        time.sleep(60)  # Sleep for 60 seconds for testing purposes


