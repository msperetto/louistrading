from psycopg import connect, rows
from config.config import DEV_ENV_CON
from common.domain.trade import Trade

def get_open_trade_pairs():
    """
    Retorna uma lista de objetos Trade correspondentes aos pares abertos na tabela Trade.
    """
    with connect(DEV_ENV_CON, row_factory=rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM trade WHERE open = true;
            """)
            result_rows = cur.fetchall()
            return [
                Trade(
                    id=row["id"],
                    open=row["open"],
                    open_time=row["open_time"],
                    close_time=row["close_time"],
                    side=row["side"],
                    pair=row["pair"],
                    profit=row["profit"],
                    spread=row["spread"],
                    roi=row["roi"],
                    strategy_id=row["strategy_id"]
                ) for row in result_rows
            ]

def get_trade_by_id(trade_id):
    """
    Retorna uma instância de Trade para o ID fornecido.
    """
    with connect(DEV_ENV_CON, row_factory=rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM trade WHERE id = %s;
            """, (trade_id,))
            row = cur.fetchone()
            if row:
                return Trade(
                    id=row["id"],
                    open=row["open"],
                    open_time=row["open_time"],
                    close_time=row["close_time"],
                    side=row["side"],
                    pair=row["pair"],
                    profit=row["profit"],
                    spread=row["spread"],
                    roi=row["roi"],
                    strategy_id=row["strategy_id"]
                )
            return None

def get_open_trade_by_pair(pair):
    """
    Retorna a instância de Trade aberta para o par fornecido.
    """
    with connect(DEV_ENV_CON, row_factory=rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM trade WHERE pair = %s AND open = true;
            """, (pair,))
            row = cur.fetchone()
            if row:
                return Trade(
                    id=row["id"],
                    open=row["open"],
                    open_time=row["open_time"],
                    close_time=row["close_time"],
                    side=row["side"],
                    pair=row["pair"],
                    profit=row["profit"],
                    spread=row["spread"],
                    roi=row["roi"],
                    strategy_id=row["strategy_id"]
                )
            return None