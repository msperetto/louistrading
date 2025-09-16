import psycopg
from config.config import DEV_ENV_CON
from common.domain.strategy import Strategy

def get_strategy_by_id(strategy_id: int) -> Strategy:
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, enabled, operation_type 
                FROM strategy 
                WHERE id = %s;
                """, (strategy_id,))
            row = cur.fetchone()
            if row:
                return Strategy(row['id'], row['name'], row['enabled'], row['operation_type'])
            return None  # Retorna None caso o ID não exista

def get_strategy_by_name(strategy_name: str) -> Strategy:
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, enabled, operation_type 
                FROM strategy 
                WHERE name = %s;
                """, (strategy_name,))
            row = cur.fetchone()
            if row:
                return Strategy(row['id'], row['name'], row['enabled'], row['operation_type'])
            return None  # Retorna None caso o nome não exista

def get_strategies(strategy_ids: list[int]) -> list[Strategy]:
    """
    Retorna uma lista de objetos Strategy com base nos IDs fornecidos.
    """
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, enabled, operation_type FROM strategy WHERE id = ANY(%s);
            """, (strategy_ids,))
            return [Strategy(row['id'], row['name'], row['enabled'], row['operation_type']) for row in cur.fetchall()]

def get_enabled_strategies_by_type(operation_type: str) -> list[Strategy]:
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, enabled, operation_type FROM strategy 
                WHERE enabled = TRUE AND operation_type = %s;
            """, (operation_type,))
            return [Strategy(row['id'], row['name'], row['enabled'], row['operation_type']) for row in cur.fetchall()]
