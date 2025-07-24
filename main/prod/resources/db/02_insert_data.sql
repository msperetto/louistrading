-- Inserção de dados nas tabelas do banco de dados

-- Tabela initial_config
INSERT INTO public.initial_config (max_open_orders, order_value, max_risk, opperation_active, leverage_long_value, leverage_short_value, use_stop_loss_orders, stop_loss_percentage, use_stop_gain_orders, stop_gain_percentage)
VALUES (5, 100, 10, 't', 1, 1, 't', 0.02, 't', 0.05);


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

-- Tabela bot_execution_control
INSERT INTO bot_execution_control (line) 
VALUES
    (1);