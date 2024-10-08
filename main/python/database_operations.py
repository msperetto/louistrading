import psycopg
import csv

dev_env_con = "dbname=noshirt user=postgres password=@tkTYB9i"

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


def get_binance_config():
    with psycopg.connect(dev_env_con, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, sk FROM config_binance;
                """)
            return cur.fetchone()


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

# export_to_csv()
# insert_class("FilterBuy_alwaysTrue", "self.filterBuy = Filter_alwaysTrue()")
# insert_class("FilterSell_alwaysTrue", "self.filterSell = Filter_alwaysTrue()")
# insert_class("TriggeredStateBuy_alwaysTrue", "self.triggerBuy = TriggeredState_alwaysTrue()")
# insert_class("TriggeredStateSell_alwaysTrue", "self.triggerSell = TriggeredState_alwaysTrue()")