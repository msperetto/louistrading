import psycopg
import csv
from datetime import datetime
from config.config import DEV_ENV_CON
from common.enums import Side_Type

# def insert_report(start_time, end_time, pair, strategy_name, return_percent, return_buy_hold, win_rate, sharpe_ratio, max_drawdown, best_indicators_combination):
def insert_report(pair, period, stats, best_indicators_combination, period_label, trend_period, strategy_class = ""):
    with psycopg.connect(DEV_ENV_CON) as conn:
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
    with psycopg.connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO classes_map(class_name, class_code)
                VALUES(%s, %s);
            """, (class_name, class_code))
            conn.commit()


def get_class_code(class_name):
    with psycopg.connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT class_code FROM classes_map WHERE class_name = %(value)s;
                """, {"value": class_name})
            return cur.fetchone()[0]


def get_active_pairs():
    with psycopg.connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT pair_code from pair where active is true;
                """)
            # code to return a list of strings instead a list of tuples
            result = [symbol[0] for symbol in cur.fetchall()]    
            return result


def insert_exchange_config(id, key, exchange: str):
    with psycopg.connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO exchange_config (id, sk, exchange) VALUES(%s, %s, %s); 
            """, (id, key, exchange))

            conn.commit()


def get_exchange_config(exchange: str):
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, sk FROM exchange_config WHERE exchange = %s;
                """,(exchange,))
            return cur.fetchone()

def get_bot_execution_control():
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM bot_execution_control WHERE line = 1;
                """)
            return cur.fetchone()

def get_initial_config():
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM initial_config;
                """)
            return cur.fetchone()
   
def insert_order_transaction(order_response, operation_type, trade_id, avgPrice,fees = 0.001, loss_stopped=False, gain_stopped=False):
    with psycopg.connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO order_control(order_id, date, pair, operation_type, side, entry_price, quantity,
                                              status, fees, trade_id, loss_stopped, gain_stopped)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (order_response['orderId'], datetime.fromtimestamp(order_response['updateTime'] / 1000), order_response['symbol'], operation_type,
                   Side_Type(order_response['side']).value.lower(), avgPrice, order_response['origQty'],
                   order_response['status'].upper(), fees, trade_id, loss_stopped, gain_stopped))
            conn.commit()

def insert_trade_transaction(strategy_id, open, order_response, profit = None, spread=None, roi=None):
    with psycopg.connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO trade(open, open_time, side, pair, strategy_id)
                VALUES(%s, %s, %s, %s, %s)
                RETURNING id, pair;
            """, (open, datetime.fromtimestamp(order_response['updateTime'] / 1000), Side_Type(order_response['side']).name, order_response['symbol'], strategy_id))
            conn.commit()
            return cur.fetchone()[0]

def get_order(trade_id):
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM order_control WHERE trade_id = %s;
                """,(trade_id,))
            return cur.fetchone()

def update_trade_transaction(trade_id, order_response, profit = None, spread=None, roi=None):
    with psycopg.connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE trade
                SET open = %s,
                    close_time = %s,
                    profit = %s,
                    spread = %s,
                    roi = %s
                WHERE id = %s;
            """, (False, datetime.fromtimestamp(order_response['updateTime'] / 1000), profit, spread, roi, trade_id))
            conn.commit()


def export_to_csv():
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM optmization_tests;
                """)
            keys = ""
            with open('noshirt_optmization.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, cur.fetchone().keys())
                writer.writeheader()
                writer.writerows(cur.fetchall())

def update_bot_execution_control():
    with psycopg.connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE bot_execution_control
                SET last_execution = %s
                WHERE line = 1;
            """, (datetime.now(),))
            conn.commit()