from psycopg import connect, rows
from config.config import DEV_ENV_CON
from common.domain.account_balance import AccountBalance

def insert_account_balance(account_id, account_balance, margin_ratio):
    with connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO account_balance (account_id, usdt_balance, margin_ratio)
                VALUES (%s, %s, %s);
            """, (
                account_id,
                account_balance,
                margin_ratio
            ))
            conn.commit()

def update_account_balance(account_id, account_balance, margin_ratio):
    with connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE account_balance
                SET usdt_balance = %s, margin_ratio = %s
                WHERE account_id = %s;
            """, (
                account_balance,
                margin_ratio,
                account_id
            ))
            conn.commit()

def get_account_balance(account_id):
    with connect(DEV_ENV_CON, row_factory=rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM account_balance WHERE account_id = %s;
            """, (account_id,))
            row = cur.fetchone()
            if row:
                return [
                    AccountBalance(
                        account_id=row["account_id"],
                        account_balance=row["usdt_balance"],
                        margin_ratio=row["margin_ratio"],
                        date_updated=row["date_updated"]
                    )
                ]            
            return None