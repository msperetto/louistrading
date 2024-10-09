--
-- PostgreSQL classes_map table repopulation, to run on every change:
-- run the following:
-- psql -U username -d noshirt -a -f classes_map_rebuild.sql
--

--
-- Data for Name: classes_map; Type: TABLE DATA; Schema: public; 
--

DELETE FROM public.classes_map;

INSERT INTO public.classes_map(class_name, class_code)
VALUES
('FilterBuy_RSI', 'self.filterBuy = FilterBuy_RSI(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap)'),
('FilterBuy_RSI_price_x_SMAlong',	'self.filterBuy = FilterBuy_RSI_price_x_SMAlong(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, self.data, lambda self=self: self.sma_long[:len(self.sma_long)])'),
('FilterBuy_RSI_price_x_SMAmedium',	'self.filterBuy = FilterBuy_RSI_price_x_SMAmedium(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, self.data, lambda self=self: self.sma_medium[:len(self.sma_medium)])'),
('FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAlong',	'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAlong(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, self.data, lambda self=self: self.sma_long[:len(self.sma_long)], lambda self=self: self.ema_short[:len(self.ema_short)])'),
('FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAmedium',	'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAmedium(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, self.data, lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_long[:len(self.sma_long)])'),
('FilterBuy_RSI_EMAshort_gt_SMAlong', 'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_long[:len(self.sma_long)])'),
('TriggeredState_MaxCandles',	'self.triggerBuy = TriggeredState_MaxCandles(self.max_candles_buy)'),
('TradeBuy_High_x_HighLastCandle',	'self.tradeBuy = TradeBuy_High_x_HighLastCandle(self.data)'),
('TradeBuy_Price_gt_EMAshort', 'self.tradeBuy = TradeBuy_Price_gt_EMAshort(self.data, lambda self=self: self.ema_short[:len(self.ema_short)])'),
('TradeBuy_Price_gt_SMAmedium', 'self.tradeBuy = TradeBuy_Price_gt_SMAmedium(self.data, lambda self=self: self.sma_medium[:len(self.sma_medium)])'),
('TradeBuy_EMAshort_gt_SMAmedium', 'self.tradeBuy = TradeBuy_EMAshort_gt_SMAmedium(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)])'),
('TradeBuy_EMAshort_gt_SMAmedium_High_gt_HighLastCandle', 'self.tradeBuy = TradeBuy_EMAshort_gt_SMAmedium_High_gt_HighLastCandle(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], self.data)'),
('TradeBuy_HighLastCandle',	'self.tradeBuy = TradeBuy_HighLastCandle(self.data)'),
('TradeBuy_Close_gt_CloseLastCandle', 'self.tradeBuy = TradeBuy_Close_gt_CloseLastCandle(self.data)'),
('FilterSell_RSI',	'self.filterSell = FilterSell_RSI(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_expensive)'),
('TriggeredState_MaxCandles_Sell',	'self.triggerSell = TriggeredState_MaxCandles(self.max_candles_sell)'),
('TradeSell_LowLastCandle',	'self.tradeSell = TradeSell_LowLastCandle(self.data)'),
('TradeSell_Price_EMAshort',	'self.tradeSell = TradeSell_Price_EMAshort(self.data, lambda self=self: self.ema_short[:len(self.ema_short)])'),
('FilterBuy_alwaysTrue', 'self.filterBuy = Filter_alwaysTrue()'),
('FilterSell_alwaysTrue', 'self.filterSell = Filter_alwaysTrue()'),
('TriggeredStateBuy_alwaysTrue', 'self.triggerBuy = TriggeredState_alwaysTrue()'),
('TriggeredStateSell_alwaysTrue', 'self.triggerSell = TriggeredState_alwaysTrue()'),
('FilterBuy_RSI_EMAshort_gt_SMAmedium', 'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)])'),
('FilterBuy_RSI_EMAshort_gt_SMAmedium_EMAshort_gt_SMAlong', 'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium_EMAshort_gt_SMAlong(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)])'),
('FilterBuy_RSI_EMAshort_gt_SMAmedium_gt_SMAlong', 'self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium_gt_SMAlong(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)])'),
('FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong', 'self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)])'),
('FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAmedium', 'self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAmedium(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)], self.data)'),
('FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAlong', 'self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAlong(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)], self.data)');