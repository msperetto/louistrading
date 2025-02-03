-- Remoção de tabelas e sequências existentes para reinicializar o banco de dados

-- Remove FKs:
DO
$$
BEGIN
    -- Remover foreign key da tabela trade
    IF EXISTS (SELECT 1 FROM information_schema.table_constraints 
               WHERE constraint_name = 'trade_pair_fkey') THEN
        ALTER TABLE ONLY public.trade DROP CONSTRAINT trade_pair_fkey;
    END IF;

    -- Remover foreign key da tabela order_control (trade_id)
    IF EXISTS (SELECT 1 FROM information_schema.table_constraints 
               WHERE constraint_name = 'order_trade_fkey') THEN
        ALTER TABLE ONLY public.order_control DROP CONSTRAINT order_trade_fkey;
    END IF;

    -- Remover foreign key da tabela order_control (pair)
    IF EXISTS (SELECT 1 FROM information_schema.table_constraints 
               WHERE constraint_name = 'order_pair_fkey') THEN
        ALTER TABLE ONLY public.order_control DROP CONSTRAINT order_pair_fkey;
    END IF;

    -- Remover foreign key da tabela order_control (pair)
    IF EXISTS (SELECT 1 FROM information_schema.table_constraints 
               WHERE constraint_name = 'trade_strategy_id_fkey') THEN
        ALTER TABLE ONLY public.trade DROP CONSTRAINT trade_strategy_id_fkey;
    END IF;

END
$$;

-- Deleta tabelas.
DROP TABLE IF EXISTS public.classes_map CASCADE;
DROP TABLE IF EXISTS public.exchange_config CASCADE;
DROP TABLE IF EXISTS public.initial_config CASCADE;
DROP TABLE IF EXISTS public.strategy CASCADE;
DROP TABLE IF EXISTS public.order_control CASCADE;
DROP TABLE IF EXISTS public.trade CASCADE;
DROP TABLE IF EXISTS public.pair CASCADE;
DROP TABLE IF EXISTS public.alert CASCADE;
DROP TABLE IF EXISTS public.account_balance CASCADE;
DROP TABLE IF EXISTS public.bot_execution_control CASCADE;


-- Deleta sequences.
DROP SEQUENCE IF EXISTS public.strategy_id_seq CASCADE;
DROP SEQUENCE IF EXISTS public.trade_id_seq CASCADE;
DROP SEQUENCE IF EXISTS public.order_id_seq CASCADE;
