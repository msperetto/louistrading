import psycopg
import csv

dev_env_con = "dbname=noshirt user=peretto"
# dev_env_con = "dbname=noshirt user=postgres password=@tkTYB9i"

# def insert_report(start_time, end_time, pair, strategy_name, return_percent, return_buy_hold, win_rate, sharpe_ratio, max_drawdown, best_indicators_combination):
def insert_report(pair, period, stats, best_indicators_combination, period_label, trend_period, strategy_class = ""):
    with psycopg.connect(dev_env_con) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO optmization_tests(start_time, end_time, pair, period, return_percent,
                                              return_buy_hold, win_rate, sharpe_ratio, max_drawdown, 
                                              best_indicators_combination, filter_buy, trigger_buy, trade_buy,
                                              filter_sell, trigger_sell, trade_sell, total_trades, best_trade,
                                              worst_trade, average_trade, profit_factor, label_period, period_trend,
                                              trend_class, strategy_class)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (stats['Start'], stats['End'],pair, period, round(stats['Return [%]'],2), round(stats['Buy & Hold Return [%]'],2),
                  round(stats['Win Rate [%]'], 2), round(stats['Sharpe Ratio'],2), round(stats['Max. Drawdown [%]'],2), best_indicators_combination,
                  stats._strategy.classes['filter_buy'], stats._strategy.classes['trigger_buy'], stats._strategy.classes['trade_buy'],
                  stats._strategy.classes['filter_sell'], stats._strategy.classes['trigger_sell'], stats._strategy.classes['trade_sell'],
                  stats['# Trades'], round(stats['Best Trade [%]'],2), round(stats['Worst Trade [%]'],2), round(stats['Avg. Trade [%]'],2),
                  round(stats['Profit Factor'],2), period_label, trend_period, stats._strategy.classes['trend'], strategy_class))
            conn.commit()

def insert_class(class_name, class_code):
    with psycopg.connect(dev_env_con) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO classes_map(class_name, class_code)
                VALUES(%s, %s);
            """, (class_name, class_code))
            conn.commit()


def get_class_code(class_name):
    with psycopg.connect(dev_env_con) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT class_code FROM classes_map WHERE class_name = %(value)s;
                """, {"value": class_name})
            return cur.fetchone()[0]


def get_active_pairs():
    with psycopg.connect(dev_env_con) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT pair_code from pair where active is true;
                """)
            return cur.fetchall()


def insert_exchange_config(id, key, exchange: str):
    with psycopg.connect(dev_env_con) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO exchange_config (id, sk, exchange) VALUES(%s, %s, %s); 
            """, (id, key, exchange))

            conn.commit()


def get_exchange_config(exchange: str):
    with psycopg.connect(dev_env_con, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, sk FROM exchange_config WHERE exchange = %s;
                """,(exchange,))
            return cur.fetchone()

def get_initial_config():
    with psycopg.connect(dev_env_con, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM initial_config;
                """)
            return cur.fetchone()

def get_open_orders():
    with psycopg.connect(dev_env_con, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT pair FROM trade WHERE open is true;
                """)
            return [pair["pair"] for pair in cur.fetchall()]

def get_strategy_id(strategy_name: str):
    with psycopg.connect(dev_env_con, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id FROM strategy WHERE name = %s;
                """,(strategy_name,))
            return cur.fetchone()['id']
   
def insert_order_transaction(order_response, operation_type, trade_id, fees = 0.001):
    with psycopg.connect(dev_env_con) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO order_control(order_id, date, pair, operation_type, side, entry_price, quantity,
                                              status, fees, trade_id)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (order_response['orderId'], order_response['updateTime'], order_response['symbol'], operation_type,
                   order_response['positionSide'], order_response['avgPrice'], order_response['origQty'],
                   order_response['status'], fees, trade_id))
            conn.commit()

def insert_trade_transaction(strategy_id, open, order_response, profit = None, spread=None, roi=None):
    with psycopg.connect(dev_env_con) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO trade(open, open_time, side, pair, strategy_id)
                VALUES(%s, %s, %s, %s, %s)
                RETURNING id, pair;
            """, (open, order_response['updateTime'], order_response['positionSide'], order_response['symbol'], strategy_id))
            conn.commit()
            return cur.fetchone()[0]


def update_trade_transaction(trade_id, strategy_id, order_response, profit = None, spread=None, roi=None):
    with psycopg.connect(dev_env_con) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE trade
                SET open = %s,
                    close_time = %s,
                    profit = %s,
                    spread = %s,
                    roi = %s
                WHERE id = %s;
            """, (False, order_response['updateTime'], profit, spread, roi, trade_id))
            conn.commit()


def export_to_csv():
    with psycopg.connect(dev_env_con, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM optmization_tests;
                """)
            keys = ""
            with open('noshirt_optmization.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, cur.fetchone().keys())
                writer.writeheader()
                writer.writerows(cur.fetchall())
