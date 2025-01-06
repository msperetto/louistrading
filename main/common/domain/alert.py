from datetime import datetime

class Alert:
    def __init__(self,
                 id: int,
                 date: datetime,
                 pair: str,
                 alert_type: str,
                 active: bool,
                 message: str):
        self.id = id
        self.date = date
        self.pair = pair
        self.alert_type = alert_type
        self.active = active
        self.message = message

    def __repr__(self):
        return (f"Alert(id={self.id}, date={self.date}, pair='{self.pair}', alert_type='{self.alert_type}', active={self.active}, "
                f"message='{self.message}')")
