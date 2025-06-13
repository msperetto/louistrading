from psycopg import connect, rows
from config.config import DEV_ENV_CON
from common.domain.backtest import Backtest

def get_backtests():
    with connect(DEV_ENV_CON, row_factory=rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM optmization_tests;
            """)
            rows = cur.fetchall()
            if rows is None:
                return []
            return [Backtest(**row) for row in rows]