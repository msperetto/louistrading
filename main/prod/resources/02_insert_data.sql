-- Inserção de dados nas tabelas do banco de dados

-- Tabela classes_map
INSERT INTO public.classes_map(class_name, class_code)
VALUES
('FilterBuy_RSI', 'self.filterBuy = FilterBuy_RSI(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap)'),
('FilterBuy_RSI_price_x_SMAlong',	'self.filterBuy = FilterBuy_RSI_price_x_SMAlong(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, self.data, lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])'),
('FilterBuy_RSI_price_x_SMAmedium',	'self.filterBuy = FilterBuy_RSI_price_x_SMAmedium(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, self.data, lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])'),
('FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAlong',	'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAlong(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, self.data, lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)], lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)])'),
('FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAmedium',	'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAmedium(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, self.data, lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])'),
('FilterBuy_RSI_EMAshort_gt_SMAlong', 'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])'),
('FilterBuy_EMAshort_gt_SMAlong', 'self.filterBuy = FilterBuy_EMAshort_gt_SMAlong(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])'),
('FilterBuy_EMAshort_gt_SMAmedium', 'self.filterBuy = FilterBuy_EMAshort_gt_SMAmedium(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])'),
('FilterBuy_SMAmedium_gt_SMAlong', 'self.filterBuy = FilterBuy_SMAmedium_gt_SMAlong(lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])'),
('FilterBuy_SMAmedium_gt_SMAlong_or_price_x_SMAlong_price_x_SMAmedium', 'self.filterBuy = FilterBuy_SMAmedium_gt_SMAlong_or_price_x_SMAlong_price_x_SMAmedium(self.data, lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])'),
('TriggeredState_MaxCandles',	'self.triggerBuy = TriggeredState_MaxCandles(self.intraday_max_candles_buy)'),
('TradeBuy_High_x_HighLastCandle',	'self.tradeBuy = TradeBuy_High_x_HighLastCandle(self.data)'),
('TradeBuy_Price_gt_EMAshort', 'self.tradeBuy = TradeBuy_Price_gt_EMAshort(self.data, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)])'),
('TradeBuy_Price_gt_SMAmedium', 'self.tradeBuy = TradeBuy_Price_gt_SMAmedium(self.data, lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])'),
('TradeBuy_EMAshort_gt_SMAmedium', 'self.tradeBuy = TradeBuy_EMAshort_gt_SMAmedium(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])'),
('TradeBuy_EMAshort_gt_SMAmedium_High_gt_HighLastCandle', 'self.tradeBuy = TradeBuy_EMAshort_gt_SMAmedium_High_gt_HighLastCandle(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], self.data)'),
('TradeBuy_HighLastCandle',	'self.tradeBuy = TradeBuy_HighLastCandle(self.data)'),
('TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium', 'self.tradeBuy = TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium(self.data, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])'),
('TradeBuy_Close_gt_CloseLastCandle', 'self.tradeBuy = TradeBuy_Close_gt_CloseLastCandle(self.data)'),
('FilterSell_RSI',	'self.filterSell = FilterSell_RSI(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_expensive)'),
('TriggeredState_MaxCandles_Sell',	'self.triggerSell = TriggeredState_MaxCandles(self.intraday_max_candles_sell)'),
('TradeSell_LowLastCandle',	'self.tradeSell = TradeSell_LowLastCandle(self.data)'),
('TradeSell_Price_EMAshort',	'self.tradeSell = TradeSell_Price_EMAshort(self.data, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)])'),
('FilterBuy_alwaysTrue', 'self.filterBuy = Filter_alwaysTrue()'),
('FilterSell_alwaysTrue', 'self.filterSell = Filter_alwaysTrue()'),
('TriggeredStateBuy_alwaysTrue', 'self.triggerBuy = TriggeredState_alwaysTrue()'),
('TriggeredStateSell_alwaysTrue', 'self.triggerSell = TriggeredState_alwaysTrue()'),
('FilterBuy_RSI_EMAshort_gt_SMAmedium', 'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])'),
('FilterBuy_RSI_EMAshort_gt_SMAmedium_EMAshort_gt_SMAlong', 'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium_EMAshort_gt_SMAlong(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])'),
('FilterBuy_RSI_EMAshort_gt_SMAmedium_gt_SMAlong', 'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium_gt_SMAlong(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])'),
('FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong', 'self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])'),
('FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAmedium', 'self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAmedium(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)], self.data)'),
('FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAlong', 'self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAlong(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)], self.data)'),
('UpTrend_AlwaysTrend', 'self.trend = UpTrend_AlwaysTrend()'),
('UpTrend_EMAshort_gt_SMAlong', 'self.trend = UpTrend_EMAshort_gt_SMAlong(lambda self=self: self.trend_ema_short[:len(self.trend_ema_short)], lambda self=self: self.trend_sma_long[:len(self.trend_sma_long)])'),
('UpTrend_EMAshort_gt_SMAmedium', 'self.trend = UpTrend_EMAshort_gt_SMAmedium(lambda self=self: self.trend_ema_short[:len(self.trend_ema_short)], lambda self=self: self.trend_sma_medium[:len(self.trend_sma_medium)])'),
('UpTrend_SMAmedium_gt_SMAlong', 'self.trend = UpTrend_SMAmedium_gt_SMAlong(lambda self=self: self.trend_sma_medium[:len(self.trend_sma_medium)], lambda self=self: self.trend_sma_long[:len(self.trend_sma_long)])'),
('UpTrend_EMAshort_gt_SMAmedium_gt_SMAlong', 'self.trend = UpTrend_EMAshort_gt_SMAmedium_gt_SMAlong(lambda self=self: self.trend_ema_short[:len(self.trend_ema_short)], lambda self=self: self.trend_sma_medium[:len(self.trend_sma_medium)], lambda self=self: self.trend_sma_long[:len(self.trend_sma_long)])'),
('UpTrend_Price_gt_SMAmedium', 'self.trend = UpTrend_Price_gt_SMAmedium(self.data, lambda self=self: self.trend_sma_medium[:len(self.trend_sma_medium)])'),
('UpTrend_Price_gt_SMAlong', 'self.trend = UpTrend_Price_gt_SMAlong(self.data, lambda self=self: self.trend_sma_long[:len(self.trend_sma_long)])'),
('UpTrend_Price_gt_EMAshort', 'self.trend = UpTrend_Price_gt_EMAshort(self.data, lambda self=self: self.trend_ema_short[:len(self.trend_ema_short)])');

-- Tabela initial_config
INSERT INTO public.initial_config (max_open_orders, order_value, max_risk, opperation_active, leverage_long_value, leverage_short_value)
VALUES (5, 100, 10, 't', 1, 1);


-- Tabela pair
INSERT INTO public.pair (pair_code, active) 
VALUES
    ('BTCUSDT', true),
    ('XRPUSDT', true),
    ('ETHUSDT', true),
    ('LTCUSDT', true),
    ('XTZUSDT', true),
    ('BCHUSDT', true),
    ('LINKUSDT', true),
    ('CHZUSDT', true),
    ('EOSUSDT', true),
    ('ADAUSDT', true),
    ('TRXUSDT', true);


-- Tabela strategy
INSERT INTO public.strategy (id, name, enabled) 
VALUES
    (1, 'Strategy_Test', true),
    (2, 'Strategy_B1', true),
    (3, 'Strategy_B2', true);