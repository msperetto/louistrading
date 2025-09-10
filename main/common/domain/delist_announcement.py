from datetime import datetime

class DelistAnnouncement:
    def __init__(self, id: int, announcement_date):
        self.id = id
        if isinstance(announcement_date, datetime):
            self.announcement_date = announcement_date.strftime("%Y-%m-%d")
        else:
            self.announcement_date = str(announcement_date)
        self.announcement_date = announcement_date

    def __repr__(self):
        return f"DelistAnnouncement(id={self.id}, announcement_date='{self.announcement_date}')"
