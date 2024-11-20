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