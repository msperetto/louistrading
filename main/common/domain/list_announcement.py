class ListAnnouncement:
    def __init__(self, id: int, text: str, captured_date: str):
        self.id = id
        self.text = text
        self.captured_date = captured_date

    def __repr__(self):
        return f"ListAnnouncement(id={self.id}, text='{self.text}', captured_date='{self.captured_date}')"