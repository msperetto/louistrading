--
-- Full database creation with table deletions
--
-- psql -U username -d noshirt -a -f full_database_creation_with_deletions.sql

-- Dumped from database version 14.15 (Ubuntu 14.15-1.pgdg22.04+1)
-- Dumped by pg_dump version 14.15 (Ubuntu 14.15-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: classes_map; Type: TABLE; Schema: public;
--

DROP TABLE IF EXISTS public.classes_map CASCADE;
DROP SEQUENCE IF EXISTS public.classes_map_class_id_seq CASCADE;
DROP TABLE IF EXISTS public.exchange_config CASCADE;
DROP TABLE IF EXISTS public.initial_config CASCADE;
DROP TABLE IF EXISTS public.optmization_tests CASCADE;
DROP SEQUENCE IF EXISTS public.optmization_tests_test_id_seq CASCADE;
DROP TABLE IF EXISTS public.order_control CASCADE;
DROP TABLE IF EXISTS public.pair CASCADE;
DROP TABLE IF EXISTS public.strategy CASCADE;
DROP SEQUENCE IF EXISTS public.strategy_id_seq CASCADE;
DROP TABLE IF EXISTS public.trade CASCADE;
DROP SEQUENCE IF EXISTS public.trade_id_seq CASCADE;

CREATE TABLE public.classes_map (
    class_name character varying(200) NOT NULL,
    class_code character varying(3000)
);



--
-- Name: exchange_config; Type: TABLE; Schema: public;
--

CREATE TABLE public.exchange_config (
    id character varying(120) NOT NULL,
    sk character varying(120) NOT NULL,
    exchange character varying(25) NOT NULL
);


--
-- Name: initial_config; Type: TABLE; Schema: public;
--

CREATE TABLE public.initial_config (
    max_open_orders integer,
    order_value real NOT NULL,
    max_risk real,
    opperating boolean,
    leverage_long_value real,
    leverage_short_value real
);


--
-- Name: optmization_tests; Type: TABLE; Schema: public;
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
-- Name: optmization_tests_test_id_seq; Type: SEQUENCE; Schema: public;
--

CREATE SEQUENCE public.optmization_tests_test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: optmization_tests_test_id_seq; Type: SEQUENCE OWNED BY; Schema: public;
--

ALTER SEQUENCE public.optmization_tests_test_id_seq OWNED BY public.optmization_tests.test_id;


--
-- Name: order_control; Type: TABLE; Schema: public;
--

CREATE TABLE public.order_control (
    order_id integer NOT NULL,
    date timestamp with time zone NOT NULL,
    pair character varying(20) NOT NULL,
    operation_type character varying(6) NOT NULL,
    side character varying(6),
    entry_price real NOT NULL,
    quantity real NOT NULL,
    status character varying(15) NOT NULL,
    fees real,
    trade_id integer DEFAULT 1 NOT NULL
);


--
-- Name: pair; Type: TABLE; Schema: public;
--

CREATE TABLE public.pair (
    pair_code character varying(25) NOT NULL,
    active boolean DEFAULT false NOT NULL
);


--
-- Name: strategy; Type: TABLE; Schema: public;
--

CREATE TABLE public.strategy (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    enabled boolean
);


--
-- Name: strategy_id_seq; Type: SEQUENCE; Schema: public;
--

CREATE SEQUENCE public.strategy_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: strategy_id_seq; Type: SEQUENCE OWNED BY; Schema: public;
--

ALTER SEQUENCE public.strategy_id_seq OWNED BY public.strategy.id;


--
-- Name: trade; Type: TABLE; Schema: public;
--

CREATE TABLE public.trade (
    id integer NOT NULL,
    open boolean NOT NULL,
    open_time timestamp with time zone NOT NULL,
    close_time timestamp with time zone,
    side character varying(5) NOT NULL,
    pair character varying(20) NOT NULL,
    profit real,
    spread real,
    roi real,
    strategy_id integer
);


--
-- Name: trade_id_seq; Type: SEQUENCE; Schema: public;
--

CREATE SEQUENCE public.trade_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trade_id_seq; Type: SEQUENCE OWNED BY; Schema: public;
--

ALTER SEQUENCE public.trade_id_seq OWNED BY public.trade.id;


--
-- Name: optmization_tests test_id; Type: DEFAULT; Schema: public;
--

ALTER TABLE ONLY public.optmization_tests ALTER COLUMN test_id SET DEFAULT nextval('public.optmization_tests_test_id_seq'::regclass);


--
-- Name: strategy id; Type: DEFAULT; Schema: public;
--

ALTER TABLE ONLY public.strategy ALTER COLUMN id SET DEFAULT nextval('public.strategy_id_seq'::regclass);


--
-- Name: trade id; Type: DEFAULT; Schema: public;
--

ALTER TABLE ONLY public.trade ALTER COLUMN id SET DEFAULT nextval('public.trade_id_seq'::regclass);


--
-- Name: classes_map classes_map_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.classes_map
    ADD CONSTRAINT classes_map_pkey PRIMARY KEY (class_name);


--
-- Name: optmization_tests optmization_tests_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.optmization_tests
    ADD CONSTRAINT optmization_tests_pkey PRIMARY KEY (test_id);


--
-- Name: order_control order_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.order_control
    ADD CONSTRAINT order_pkey PRIMARY KEY (order_id, pair);


--
-- Name: pair pair_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.pair
    ADD CONSTRAINT pair_pkey PRIMARY KEY (pair_code);


--
-- Name: strategy strategy_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.strategy
    ADD CONSTRAINT strategy_pkey PRIMARY KEY (id);


--
-- Name: trade trade_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.trade
    ADD CONSTRAINT trade_pkey PRIMARY KEY (id);


--
-- Name: order_control trade_fkey; Type: FK CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.order_control
    ADD CONSTRAINT trade_fkey FOREIGN KEY (trade_id) REFERENCES public.trade(id);


--
-- Name: trade trade_strategy_id_fkey; Type: FK CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.trade
    ADD CONSTRAINT trade_strategy_id_fkey FOREIGN KEY (strategy_id) REFERENCES public.strategy(id);


--
-- Data for Name: classes_map; Type: TABLE DATA; Schema: public;
--

COPY public.classes_map (class_name, class_code) FROM stdin;
FilterBuy_RSI	self.filterBuy = FilterBuy_RSI(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap)
FilterBuy_RSI_price_x_SMAlong	self.filterBuy = FilterBuy_RSI_price_x_SMAlong(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, self.data, lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])
FilterBuy_RSI_price_x_SMAmedium	self.filterBuy = FilterBuy_RSI_price_x_SMAmedium(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, self.data, lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])
FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAlong	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAlong(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, self.data, lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)], lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)])
FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAmedium	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong_price_x_SMAmedium(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, self.data, lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])
FilterBuy_RSI_EMAshort_gt_SMAlong	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAlong(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])
FilterBuy_EMAshort_gt_SMAlong	self.filterBuy = FilterBuy_EMAshort_gt_SMAlong(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])
FilterBuy_EMAshort_gt_SMAmedium	self.filterBuy = FilterBuy_EMAshort_gt_SMAmedium(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])
FilterBuy_SMAmedium_gt_SMAlong	self.filterBuy = FilterBuy_SMAmedium_gt_SMAlong(lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])
FilterBuy_SMAmedium_gt_SMAlong_or_price_x_SMAlong_price_x_SMAmedium	self.filterBuy = FilterBuy_SMAmedium_gt_SMAlong_or_price_x_SMAlong_price_x_SMAmedium(self.data, lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])
TriggeredState_MaxCandles	self.triggerBuy = TriggeredState_MaxCandles(self.intraday_max_candles_buy)
TradeBuy_High_x_HighLastCandle	self.tradeBuy = TradeBuy_High_x_HighLastCandle(self.data)
TradeBuy_Price_gt_EMAshort	self.tradeBuy = TradeBuy_Price_gt_EMAshort(self.data, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)])
TradeBuy_Price_gt_SMAmedium	self.tradeBuy = TradeBuy_Price_gt_SMAmedium(self.data, lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])
TradeBuy_EMAshort_gt_SMAmedium	self.tradeBuy = TradeBuy_EMAshort_gt_SMAmedium(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])
TradeBuy_EMAshort_gt_SMAmedium_High_gt_HighLastCandle	self.tradeBuy = TradeBuy_EMAshort_gt_SMAmedium_High_gt_HighLastCandle(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], self.data)
TradeBuy_HighLastCandle	self.tradeBuy = TradeBuy_HighLastCandle(self.data)
TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium	self.tradeBuy = TradeBuy_HighLastCandle_EMAshort_gt_SMAmedium(self.data, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])
TradeBuy_Close_gt_CloseLastCandle	self.tradeBuy = TradeBuy_Close_gt_CloseLastCandle(self.data)
FilterSell_RSI	self.filterSell = FilterSell_RSI(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_expensive)
TriggeredState_MaxCandles_Sell	self.triggerSell = TriggeredState_MaxCandles(self.intraday_max_candles_sell)
TradeSell_LowLastCandle	self.tradeSell = TradeSell_LowLastCandle(self.data)
TradeSell_Price_EMAshort	self.tradeSell = TradeSell_Price_EMAshort(self.data, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)])
FilterBuy_alwaysTrue	self.filterBuy = Filter_alwaysTrue()
FilterSell_alwaysTrue	self.filterSell = Filter_alwaysTrue()
TriggeredStateBuy_alwaysTrue	self.triggerBuy = TriggeredState_alwaysTrue()
TriggeredStateSell_alwaysTrue	self.triggerSell = TriggeredState_alwaysTrue()
FilterBuy_RSI_EMAshort_gt_SMAmedium	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)])
FilterBuy_RSI_EMAshort_gt_SMAmedium_EMAshort_gt_SMAlong	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium_EMAshort_gt_SMAlong(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])
FilterBuy_RSI_EMAshort_gt_SMAmedium_gt_SMAlong	self.filterBuy = FilterBuy_RSI_EMAshort_gt_SMAmedium_gt_SMAlong(lambda self=self: self.intraday_rsi[:len(self.intraday_rsi)], self.intraday_rsi_layer_cheap, lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])
FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong	self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)])
FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAmedium	self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAmedium(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)], self.data)
FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAlong	self.filterBuy = FilterBuy_EMAshort_lt_SMAmedium_gt_SMAlong_Price_gt_SMAlong(lambda self=self: self.intraday_ema_short[:len(self.intraday_ema_short)], lambda self=self: self.intraday_sma_medium[:len(self.intraday_sma_medium)], lambda self=self: self.intraday_sma_long[:len(self.intraday_sma_long)], self.data)
UpTrend_AlwaysTrend	self.trend = UpTrend_AlwaysTrend()
UpTrend_EMAshort_gt_SMAlong	self.trend = UpTrend_EMAshort_gt_SMAlong(lambda self=self: self.trend_ema_short[:len(self.trend_ema_short)], lambda self=self: self.trend_sma_long[:len(self.trend_sma_long)])
UpTrend_EMAshort_gt_SMAmedium	self.trend = UpTrend_EMAshort_gt_SMAmedium(lambda self=self: self.trend_ema_short[:len(self.trend_ema_short)], lambda self=self: self.trend_sma_medium[:len(self.trend_sma_medium)])
UpTrend_SMAmedium_gt_SMAlong	self.trend = UpTrend_SMAmedium_gt_SMAlong(lambda self=self: self.trend_sma_medium[:len(self.trend_sma_medium)], lambda self=self: self.trend_sma_long[:len(self.trend_sma_long)])
UpTrend_EMAshort_gt_SMAmedium_gt_SMAlong	self.trend = UpTrend_EMAshort_gt_SMAmedium_gt_SMAlong(lambda self=self: self.trend_ema_short[:len(self.trend_ema_short)], lambda self=self: self.trend_sma_medium[:len(self.trend_sma_medium)], lambda self=self: self.trend_sma_long[:len(self.trend_sma_long)])
UpTrend_Price_gt_SMAmedium	self.trend = UpTrend_Price_gt_SMAmedium(self.data, lambda self=self: self.trend_sma_medium[:len(self.trend_sma_medium)])
UpTrend_Price_gt_SMAlong	self.trend = UpTrend_Price_gt_SMAlong(self.data, lambda self=self: self.trend_sma_long[:len(self.trend_sma_long)])
UpTrend_Price_gt_EMAshort	self.trend = UpTrend_Price_gt_EMAshort(self.data, lambda self=self: self.trend_ema_short[:len(self.trend_ema_short)])
\.

--
-- Data for Name: initial_config; Type: TABLE DATA; Schema: public;
--

COPY public.initial_config (max_open_orders, order_value, max_risk, opperating) FROM stdin;
5	200	10	t 1 1
\.

--
-- Data for Name: pair; Type: TABLE DATA; Schema: public;
--

COPY public.pair (pair_code, active) FROM stdin;
BTCUSDT	t
XRPUSDT	f
ETHUSDT	t
\.

--
-- Data for Name: strategy; Type: TABLE DATA; Schema: public;
--

COPY public.strategy (id, name, enabled) FROM stdin;
1	Strategy_B1	t
2	Strategy_Test	t
\.


--
-- Name: strategy_id_seq; Type: SEQUENCE SET; Schema: public;
--

SELECT pg_catalog.setval('public.strategy_id_seq', 1, false);

