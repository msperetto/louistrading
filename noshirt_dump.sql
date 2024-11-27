--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-1.pgdg22.04+1)
-- Dumped by pg_dump version 14.13 (Ubuntu 14.13-1.pgdg22.04+1)
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET xmloption = content;

SET default_table_access_method = heap;

--
-- Name: classes_map; Type: TABLE; Schema: public; Owner: 
--

CREATE TABLE public.classes_map (
    class_name character varying(200) NOT NULL,
    class_code character varying(3000)
);


--
-- Name: exchange_config; Type: TABLE; Schema: public; Owner: 
--

CREATE TABLE public.exchange_config (
    id character varying(120) NOT NULL,
    sk character varying(120) NOT NULL,
    exchange character varying(25) NOT NULL
);



--
-- Name: initial_config; Type: TABLE; Schema: public; Owner: 
--

CREATE TABLE public.initial_config (
    max_open_orders integer,
    order_value real NOT NULL,
    max_risk real
);



--
-- Name: optmization_tests; Type: TABLE; Schema: public; Owner: 
--

CREATE TABLE public.optmization_tests (
    test_id integer NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL,
    pair character varying(15) NOT NULL,
    period character varying(10) NOT NULL,
    return_percent real,
    return_buy_hold real,
    win_rate real,
    sharpe_ratio real,
    max_drawdown real,
    best_indicators_combination character varying(6000) NOT NULL,
    filter_buy character varying(255) NOT NULL,
    trigger_buy character varying(255) NOT NULL,
    trade_buy character varying(255) NOT NULL,
    filter_sell character varying(255) NOT NULL,
    trigger_sell character varying(255) NOT NULL,
    trade_sell character varying(255) NOT NULL,
    total_trades integer,
    best_trade real,
    worst_trade real,
    average_trade real,
    profit_factor real,
    created_at timestamp without time zone DEFAULT now(),
    label_period character varying(300),
    period_trend character varying(5),
    trend_class character varying(255),
    strategy_class character varying(255)
);



--
-- Name: optmization_tests_test_id_seq; Type: SEQUENCE; Schema: public; Owner: 
--

CREATE SEQUENCE public.optmization_tests_test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: optmization_tests_test_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: 
--

ALTER SEQUENCE public.optmization_tests_test_id_seq OWNED BY public.optmization_tests.test_id;


--
-- Name: pair; Type: TABLE; Schema: public; Owner: 
--

CREATE TABLE public.pair (
    pair_id integer NOT NULL,
    pair_code character varying(25) NOT NULL,
    active boolean DEFAULT false NOT NULL,
);



--
-- Name: pair_pair_id_seq; Type: SEQUENCE; Schema: public; Owner: 
--

CREATE SEQUENCE public.pair_pair_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: pair_pair_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: 
--

ALTER SEQUENCE public.pair_pair_id_seq OWNED BY public.pair.pair_id;


--
-- Name: pair_status; Type: TABLE; Schema: public; Owner: 
--




--
-- Name: optmization_tests test_id; Type: DEFAULT; Schema: public; Owner: 
--

ALTER TABLE ONLY public.optmization_tests ALTER COLUMN test_id SET DEFAULT nextval('public.optmization_tests_test_id_seq'::regclass);


--
-- Name: pair pair_id; Type: DEFAULT; Schema: public; Owner: 
--

ALTER TABLE ONLY public.pair ALTER COLUMN pair_id SET DEFAULT nextval('public.pair_pair_id_seq'::regclass);


--
-- Data for Name: classes_map; Type: TABLE DATA; Schema: public; Owner: 
--

COPY public.classes_map (class_name, class_code) FROM stdin;
FilterBuy_RSI	self.filterBuy = FilterBuy_RSI(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap)
FilterBuy_RSI_price_x_SMAlong	self.filterBuy = FilterBuy_RSI_price_x_SMAlong(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, self.data, lambda self=self: self.sma_long[:len(self.sma_long)])
FilterBuy_RSI_price_x_SMAmedium	self.filterBuy = FilterBuy_RSI_price_x_SMAmedium(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, self.data, lambda self=self: self.sma_medium[:len(self.sma_medium)])
FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAlong	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAlong(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, self.data, lambda self=self: self.sma_long[:len(self.sma_long)], lambda self=self: self.ema_short[:len(self.ema_short)])
FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAmedium	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAmedium(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, self.data, lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_long[:len(self.sma_long)])
FilterBuy_RSI_EMAshort_gt_SMAlong	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_long[:len(self.sma_long)])
FilterBuy_EMAshort_gt_SMAlong	self.filterBuy = FilterBuy_EMAshort_gt_SMAlong(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_long[:len(self.sma_long)])
FilterBuy_EMAshort_gt_SMAmedium	self.filterBuy = FilterBuy_EMAshort_gt_SMAmedium(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)])
FilterBuy_SMAmedium_gt_SMAlong	self.filterBuy = FilterBuy_SMAmedium_gt_SMAlong(lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)])
FilterBuy_SMAmedium_gt_SMAlong_or_price_x_SMAlong_price_x_SMAmedium	self.filterBuy = FilterBuy_SMAmedium_gt_SMAlong_or_price_x_SMAlong_price_x_SMAmedium(self.data, lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)])
TriggeredState_MaxCandles	self.triggerBuy = TriggeredState_MaxCandles(self.max_candles_buy)
TradeBuy_High_x_HighLastCandle	self.tradeBuy = TradeBuy_High_x_HighLastCandle(self.data)
TradeBuy_Price_gt_EMAshort	self.tradeBuy = TradeBuy_Price_gt_EMAshort(self.data, lambda self=self: self.ema_short[:len(self.ema_short)])
TradeBuy_Price_gt_SMAmedium	self.tradeBuy = TradeBuy_Price_gt_SMAmedium(self.data, lambda self=self: self.sma_medium[:len(self.sma_medium)])
TradeBuy_EMAshort_gt_SMAmedium	self.tradeBuy = TradeBuy_EMAshort_gt_SMAmedium(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)])
TradeBuy_EMAshort_gt_SMAmedium_High_gt_HighLastCandle	self.tradeBuy = TradeBuy_EMAshort_gt_SMAmedium_High_gt_HighLastCandle(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], self.data)
TradeBuy_HighLastCandle	self.tradeBuy = TradeBuy_HighLastCandle(self.data)
TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium	self.tradeBuy = TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium(self.data, lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)])
TradeBuy_Close_gt_CloseLastCandle	self.tradeBuy = TradeBuy_Close_gt_CloseLastCandle(self.data)
FilterSell_RSI	self.filterSell = FilterSell_RSI(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_expensive)
TriggeredState_MaxCandles_Sell	self.triggerSell = TriggeredState_MaxCandles(self.max_candles_sell)
TradeSell_LowLastCandle	self.tradeSell = TradeSell_LowLastCandle(self.data)
TradeSell_Price_EMAshort	self.tradeSell = TradeSell_Price_EMAshort(self.data, lambda self=self: self.ema_short[:len(self.ema_short)])
FilterBuy_alwaysTrue	self.filterBuy = Filter_alwaysTrue()
FilterSell_alwaysTrue	self.filterSell = Filter_alwaysTrue()
TriggeredStateBuy_alwaysTrue	self.triggerBuy = TriggeredState_alwaysTrue()
TriggeredStateSell_alwaysTrue	self.triggerSell = TriggeredState_alwaysTrue()
FilterBuy_RSI_EMAshort_gt_SMAmedium	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)])
FilterBuy_RSI_EMAshort_gt_SMAmedium_EMAshort_gt_SMAlong	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium_EMAshort_gt_SMAlong(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)])
FilterBuy_RSI_EMAshort_gt_SMAmedium_gt_SMAlong	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium_gt_SMAlong(lambda self=self: self.rsi[:len(self.rsi)], self.rsi_layer_cheap, lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)])
FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong	self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)])
FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAmedium	self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAmedium(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)], self.data)
FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAlong	self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAlong(lambda self=self: self.ema_short[:len(self.ema_short)], lambda self=self: self.sma_medium[:len(self.sma_medium)], lambda self=self: self.sma_long[:len(self.sma_long)], self.data)
UpTrend_AlwaysTrend	self.trend = UpTrend_AlwaysTrend()
UpTrend_EMAshort_gt_SMAlong	self.trend = UpTrend_EMAshort_gt_SMAlong(lambda self=self: self.ema_trend_short[:len(self.ema_trend_short)], lambda self=self: self.sma_trend_long[:len(self.sma_trend_long)])
UpTrend_EMAshort_gt_SMAmedium	self.trend = UpTrend_EMAshort_gt_SMAmedium(lambda self=self: self.ema_trend_short[:len(self.ema_trend_short)], lambda self=self: self.sma_trend_medium[:len(self.sma_trend_medium)])
UpTrend_SMAmedium_gt_SMAlong	self.trend = UpTrend_SMAmedium_gt_SMAlong(lambda self=self: self.sma_trend_medium[:len(self.sma_trend_medium)], lambda self=self: self.sma_trend_long[:len(self.sma_trend_long)])
UpTrend_EMAshort_gt_SMAmedium_gt_SMAlong	self.trend = UpTrend_EMAshort_gt_SMAmedium_gt_SMAlong(lambda self=self: self.ema_trend_short[:len(self.ema_trend_short)], lambda self=self: self.sma_trend_medium[:len(self.sma_trend_medium)], lambda self=self: self.sma_trend_long[:len(self.sma_trend_long)])
UpTrend_Price_gt_SMAmedium	self.trend = UpTrend_Price_gt_SMAmedium(self.data, lambda self=self: self.sma_trend_medium[:len(self.sma_trend_medium)])
UpTrend_Price_gt_SMAlong	self.trend = UpTrend_Price_gt_SMAlong(self.data, lambda self=self: self.sma_trend_long[:len(self.sma_trend_long)])
UpTrend_Price_gt_EMAshort	self.trend = UpTrend_Price_gt_EMAshort(self.data, lambda self=self: self.ema_trend_short[:len(self.ema_trend_short)])
\.



--
-- Data for Name: pair; Type: TABLE DATA; Schema: public; Owner: 
--

COPY public.pair (pair_id, pair_code, active, status_id) FROM stdin;
1	BTCUSDT	t	0
2	ETHUSDT	t	0
3	XRPUSDT	t	0
4	DOGEUSDT	f	0
\.



--
-- Name: optmization_tests_test_id_seq; Type: SEQUENCE SET; Schema: public; Owner: 
--

SELECT pg_catalog.setval('public.optmization_tests_test_id_seq', 1, true);


--
-- Name: pair_pair_id_seq; Type: SEQUENCE SET; Schema: public; Owner: 
--

SELECT pg_catalog.setval('public.pair_pair_id_seq', 3, true);


--
-- Name: classes_map classes_map_pkey; Type: CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY public.classes_map
    ADD CONSTRAINT classes_map_pkey PRIMARY KEY (class_name);


--
-- Name: optmization_tests optmization_tests_pkey; Type: CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY public.optmization_tests
    ADD CONSTRAINT optmization_tests_pkey PRIMARY KEY (test_id);


--
-- Name: pair pair_pkey; Type: CONSTRAINT; Schema: public; Owner: 
--

ALTER TABLE ONLY public.pair
    ADD CONSTRAINT pair_pkey PRIMARY KEY (pair_id);


--
-- PostgreSQL database dump complete
--

