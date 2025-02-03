-- Criação das tabelas e sequências, garantindo que só sejam criadas se não existirem

-- Tabela classes_map
CREATE TABLE IF NOT EXISTS public.classes_map (
    class_name character varying(200) NOT NULL,
    class_code character varying,
    PRIMARY KEY (class_name)
);


-- Tabela exchange_config
CREATE TABLE IF NOT EXISTS public.exchange_config (
    id character varying NOT NULL,
    sk character varying NOT NULL,
    exchange character varying(100) NOT NULL
);


-- Tabela initial_config
CREATE TABLE IF NOT EXISTS public.initial_config (
    max_open_orders integer,
    order_value real NOT NULL,
    max_risk real,
    opperation_active boolean,
    leverage_long_value real,
    leverage_short_value real
);

-- Tabela pair
CREATE TABLE IF NOT EXISTS public.pair (
    pair_code character varying(25) NOT NULL,
    active boolean DEFAULT false NOT NULL,
    PRIMARY KEY (pair_code)
);


DO $$
BEGIN
    -- Sequência strategy_id_seq
    IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'strategy_id_seq') THEN
        CREATE SEQUENCE public.strategy_id_seq
            AS INTEGER
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1;
    END IF;

    -- Tabela strategy
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'strategy') THEN
        CREATE TABLE public.strategy (
            id INTEGER NOT NULL DEFAULT nextval('public.strategy_id_seq'),
            name CHARACTER VARYING(100) NOT NULL,
            enabled BOOLEAN,
            PRIMARY KEY (id)
        );
    END IF;
END
$$;



DO
$$
BEGIN
    -- Sequência trade_id_seq
    IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'trade_id_seq') THEN
        CREATE SEQUENCE public.trade_id_seq
            AS INTEGER
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1;
    END IF;

    -- Tabela trade
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'trade') THEN
        CREATE TABLE public.trade (
            id INTEGER NOT NULL DEFAULT nextval('public.trade_id_seq'),
            open BOOLEAN NOT NULL,
            open_time TIMESTAMP WITH TIME ZONE NOT NULL,
            close_time TIMESTAMP WITH TIME ZONE,
            side CHARACTER VARYING(5) NOT NULL,
            pair CHARACTER VARYING(20) NOT NULL,
            profit REAL,
            spread REAL,
            roi REAL,
            strategy_id INTEGER,
            PRIMARY KEY (id)
        );

        ALTER TABLE ONLY public.trade
            ADD CONSTRAINT trade_strategy_id_fkey FOREIGN KEY (strategy_id) REFERENCES public.strategy(id);

        -- Foreign Key referente a coluna pair
        ALTER TABLE ONLY public.trade
            ADD CONSTRAINT trade_pair_fkey FOREIGN KEY (pair) REFERENCES public.pair(pair_code);
    END IF;
END
$$;


DO $$
BEGIN
    -- Criar a sequência apenas se ela não existir
    IF NOT EXISTS (SELECT 1 FROM information_schema.sequences WHERE sequence_schema = 'public' AND sequence_name = 'order_id_seq') THEN
        CREATE SEQUENCE public.order_id_seq
            AS INTEGER
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1;
    END IF;

    -- Criar a tabela apenas se ela não existir
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'order_control') THEN
        CREATE TABLE public.order_control (
            id INTEGER NOT NULL DEFAULT nextval('public.order_id_seq'), -- Usando a sequência
            order_id INTEGER NOT NULL,
            date TIMESTAMP WITH TIME ZONE NOT NULL,
            pair CHARACTER VARYING(20) NOT NULL,
            operation_type CHARACTER VARYING(6) NOT NULL,
            side CHARACTER VARYING(6),
            entry_price REAL NOT NULL,
            quantity REAL NOT NULL,
            status CHARACTER VARYING(15) NOT NULL,
            fees REAL,
            trade_id INTEGER NOT NULL,
            PRIMARY KEY (id)
        );

        -- Foreign Key referente a coluna trade_id
        ALTER TABLE ONLY public.order_control
            ADD CONSTRAINT order_trade_fkey FOREIGN KEY (trade_id) REFERENCES public.trade(id);

        -- Foreign Key referente a coluna pair
        ALTER TABLE ONLY public.order_control
            ADD CONSTRAINT order_pair_fkey FOREIGN KEY (pair) REFERENCES public.pair(pair_code);
    END IF;
END
$$;

-- Tabela initial_config
CREATE TABLE IF NOT EXISTS public.alert (
    id serial,
    date timestamp with time zone DEFAULT now(),
    pair varchar(20) NOT NULL,
    alert_type varchar(100) NOT NULL,
    active boolean NOT NULL,
    message text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.account_balance (
    account_id INT,
    usdt_balance real NOT NULL,
    margin_ratio real NOT NULL,
    last_update timestamp with time zone NOT NULL DEFAULT now(),
    PRIMARY KEY (account_id)
);

CREATE TABLE IF NOT EXISTS public.bot_execution_control(
    last_execution timestamp with time zone NOT NULL DEFAULT now(),
    PRIMARY KEY (last_execution)
);