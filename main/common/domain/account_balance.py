from datetime import datetime

class AccountBalance:
    def __init__(self,
                 account_id: int,
                 account_balance: float,
                 margin_ratio: float,
                 date_updated: datetime):
        self.account_id = account_id
        self.account_balance = account_balance
        self.margin_ratio = margin_ratio
        self.date_updated = date_updated

    def __repr__(self):
        return (f"Account_balance(account_id={self.account_id}, account_balance={self.account_balance}, margin_ratio={self.margin_ratio}, "
                f"dare_updated={self.date_updated})")
