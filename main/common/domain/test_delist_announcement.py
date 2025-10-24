from datetime import datetime
from typing import List, Optional

class TestDelistAnnouncement:
    def __init__(self, id: int, title: str, announcement_date: str, coins: List[str], 
                 created_at: datetime, processed: bool, notes: Optional[str] = None):
        self.id = id
        self.title = title
        self.announcement_date = announcement_date
        self.coins = coins
        self.created_at = created_at
        self.processed = processed
        self.notes = notes

    def __repr__(self):
        return f"TestDelistAnnouncement(id={self.id}, title='{self.title}', coins={self.coins}, processed={self.processed})"
