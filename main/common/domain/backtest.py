from datetime import datetime


class Backtest():
    """
    Represents a backtest configuration.
    """

    def __init__(self,
                test_id: int = None,
                start_time: datetime = None,
                end_time: datetime = None,
                pair: str = None,
                period: str = None,
                return_percent: float = None,
                return_buy_hold: float = None,
                win_rate: float = None,
                sharpe_ratio: float = None,
                max_drawdown: float = None,
                best_indicators_combination: str = None,
                filter_buy: str = None,
                trigger_buy: str = None,
                trade_buy: str = None,
                filter_sell: str = None,
                trigger_sell: str = None,
                trade_sell: str = None,
                total_trades: int = None,
                best_trade: float = None,
                worst_trade: float = None,
                average_trade: float = None,
                profit_factor: float = None,
                created_at: datetime = None,
                label_period: str = None,
                period_trend: str = None,
                trend_class: str = None,
                strategy_class: str = None):
        self.test_id = test_id
        self.start_time = start_time
        self.end_time = end_time
        self.pair = pair
        self.period = period
        self.return_percent = return_percent
        self.return_buy_hold = return_buy_hold
        self.win_rate = win_rate
        self.sharpe_ratio = sharpe_ratio
        self.max_drawdown = max_drawdown
        self.best_indicators_combination = best_indicators_combination
        self.filter_buy = filter_buy
        self.trigger_buy = trigger_buy
        self.trade_buy = trade_buy
        self.filter_sell = filter_sell
        self.trigger_sell = trigger_sell
        self.trade_sell = trade_sell
        self.total_trades = total_trades
        self.best_trade = best_trade
        self.worst_trade = worst_trade
        self.average_trade = average_trade
        self.profit_factor = profit_factor
        self.created_at = created_at if created_at else datetime.now()
        self.label_period = label_period
        self.period_trend = period_trend
        self.trend_class = trend_class
        self.strategy_class = strategy_class

    def __repr__(self):
        return (f"Backtest(test_id={self.test_id}, start_time={self.start_time}, end_time={self.end_time}, "
                f"pair='{self.pair}', period='{self.period}', return_percent={self.return_percent}, "
                f"return_buy_hold={self.return_buy_hold}, win_rate={self.win_rate}, sharpe_ratio={self.sharpe_ratio}, "
                f"max_drawdown={self.max_drawdown}, best_indicators_combination='{self.best_indicators_combination}', "
                f"filter_buy='{self.filter_buy}', trigger_buy='{self.trigger_buy}', trade_buy='{self.trade_buy}', "
                f"filter_sell='{self.filter_sell}', trigger_sell='{self.trigger_sell}', trade_sell='{self.trade_sell}', "
                f"total_trades={self.total_trades}, best_trade={self.best_trade}, worst_trade={self.worst_trade}, "
                f"average_trade={self.average_trade}, profit_factor={self.profit_factor}, created_at={self.created_at}, "
                f"label_period='{self.label_period}', period_trend='{self.period_trend}', trend_class='{self.trend_class}', "
                f"strategy_class='{self.strategy_class}')")
