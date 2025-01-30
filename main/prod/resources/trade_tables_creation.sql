-- psql -U username -d noshirt -a -f trade_tables_creation.sql

CREATE TABLE IF NOT EXISTS pair_status (
    status_id int primary key not null,
    status varchar(25)
);

CREATE TABLE IF NOT EXISTS pair (
    pair_id serial primary key,
    pair_code varchar(25) not null,
    active boolean not null default false,
    status_id int REFERENCES pair_status (status_id)
);

CREATE TABLE IF NOT EXISTS exchange_config (
    id varchar(120) NOT NULL,
    sk varchar(120) NOT NULL,
    exchange varchar(25) NOT NULL
)

CREATE TABLE IF NOT EXISTS initial_config (
    exchange varchar(25) NOT NULL,
    pair varchar(30) NOT NULL,
    intraday_interval varchar(5) NOT NULL,
    trend_interval varchar(5) NOT NULL,
    trend_class varchar(60) NOT NULL,
    strategy_class varchar(3) NOT NULL,
    max_open_orders integer,
    order_value real NOT NULL,
    max_risk real
);


DELETE FROM public.pair_status;

INSERT INTO public.pair_status(status_id, status)
VALUES
(0, 'available'),
(1, 'long'),
(2, 'short');

INSERT INTO public.pair(pair_code, active, status_id)
VALUES
('BTCUSDT', true, 0),
('ETHUSDT', true, 0),
('XRPUSDT', true, 0);