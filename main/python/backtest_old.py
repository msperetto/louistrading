from filter import Filter, FilterBuy_RSI, FilterBuy_RSI_SMA
from trigger import TriggeredState, TriggeredState_MaxCandles, TriggeredState_MaxCandles_LongSma
from trade import Trade, Trade_Buy_HighLastCandle, Trade_Sell_LowLastCandle
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas_ta as ta
import pandas as pd

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()


class PlaygroundLouis(Strategy):
    sma_period_medium = 0
    sma_period_long = 0
    rsi_period = 0
    rsi_layer_cheap = 0
    rsi_layer_expensive = 0
    triggered = False
    candles_after_triggered = 0
    max_candles = 0

    def init(self):
        self.sma1 = self.I(ta.sma, pd.Series(self.data.Close), self.sma_period_medium)
        self.sma2 = self.I(ta.sma, pd.Series(self.data.Close), self.sma_period_long)
        # self.sma1 = self.I(SMA, self.data.Close, self.sma_period1)
        self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_period)

    def next(self):
        self.strategy_trigger_only_rsi
    
    ''' Old code
    def strategy_rsi_sma(self):
        self.buy_rsi_2smas()
        self.sell_rsi()

    def strategy_trigger(self):
        self.buy_triggered_rsi_2smas()
        self.sell_rsi()       

    def strategy_trigger_only_rsi(self):
        self.buy_triggered_rsi()
        self.sell_rsi()
        '''
    
    #todo: criar uma função para buy, com as 3 fases(condição ok para compra, gestão de engatilhamento, confirmação de compra) e 
    # passar como parametro ou como objeto as possíveis funções respectivas para cada fase;

    ##### BUYING CONDITIONS FUNCTIONS #######

    def buy_rsi_2smas(self):
        """Buy when current RSI is lower then the cheap RSI layer and 
           when SMA with smaller period is bigger then a longer SMA
        """
        if (self.rsi < self.rsi_layer_cheap) and (self.sma1 > self.sma2):
            self.buy() # não retornar buy, ao invés disso, True or False para facilitar reuso;


    def buy_triggered_rsi_2smas(self):
        """Trigger when current RSI is lower then the cheap RSI layer and 
           when SMA with smaller period is bigger then a longer SMA;

           Buy when specific 
        """
        # condition from technical analysis to trigger a possible buy
        if (self.rsi < self.rsi_layer_cheap) and (self.sma1 > self.sma2):
            self.triggered = True

        self.trigger_by_candle_qtt(5) #management of trigger/untrigger conditions

        # buying if triggered and meeting conditions
        if self.triggered and (self.data.Close[-1] > self.data.High[-2]):
            self.buy()


    def buy_triggered_rsi(self):
        # condition from technical analysis to trigger a possible buy
        if (self.rsi < self.rsi_layer_cheap):
            self.triggered = True

        self.trigger_by_candle_qtt(5) #management of trigger/untrigger conditions
        
        # buying if triggered and meeting conditions
        if self.triggered and (self.data.Close[-1] > self.data.High[-2]):
            self.buy()
    
    def buy_rsi_sma_higher_price(self):
        """Buy when current RSI is lower then the cheap RSI layer and 
           when closing price higher then long SMA
        """
        if (self.rsi < self.rsi_layer_cheap) and (self.data.Close[-1] > self.sma2):
            self.buy()

    ##### SELLING CONDITIONS FUNCTIONS #######

    def sell_rsi(self):
        if self.rsi > self.rsi_layer_expensive:
            self.position.close()


    def sell_price_higher_last_high(self):
        """Sell when current closing price is smaller then lowest price of last candle
        """
        if (self.data.Close[-1] < self.data.Low[-2]):
            self.position.close()


    ##### TRIGGER MANAGEMENT FUNCTIONS #####

    def trigger_by_candle_qtt(self, max_candles):

        # starting to count the next candles after triggered
        if self.triggered and self.candles_after_triggered < max_candles:
            self.candles_after_triggered += 1
        
        # untriggering after max_candles
        elif self.candles_after_triggered >= max_candles:
            self.candles_after_triggered = 0
            self.triggered = False 


class StrategyBuy():
    def __init__(self):
        self.filter = FilterBuy_RSI()

  
    def run():
        pass


class StrategySell():
    def __init__():
        pass


    def run():
        pass