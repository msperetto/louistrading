import psycopg

dev_env_con = "dbname=noshirt user=peretto"

# def insert_report(start_time, end_time, pair, strategy_name, return_percent, return_buy_hold, win_rate, sharpe_ratio, max_drawdown, best_indicators_combination):
def insert_report(pair, strategy_name, stats, best_indicators_combination):
    with psycopg.connect(dev_env_con) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO optmization_tests(start_time, end_time, pair, strategy_name, return_percent, return_buy_hold, win_rate, sharpe_ratio, max_drawdown, best_indicators_combination)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (stats['Start'], stats['End'],pair, strategy_name, stats['Return [%]'], stats['Buy & Hold Return [%]'], stats['Win Rate [%]'], stats['Sharpe Ratio'], stats['Max. Drawdown [%]'], best_indicators_combination))
            conn.commit()


def get_binance_config():
    with psycopg.connect(dev_env_con, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, sk FROM config_binance;
                """)
            return cur.fetchone()