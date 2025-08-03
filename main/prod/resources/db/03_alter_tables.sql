-- Alteração em tabelas já existentes em produção.

-- 1. Alteração da coluna order_id na tabela order_control para bigint
DO $$ 
BEGIN
    -- Step 1: Check if the column order_id is already of type bigint
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'order_control'
          AND column_name = 'order_id'
          AND udt_name = 'int8' -- 'int8' corresponds to bigint in PostgreSQL
    ) THEN
        -- Do nothing if the column is already bigint
        RAISE NOTICE 'Column order_id is already of type bigint.';
    ELSE
        -- Step 2: Create a new column with a temporary name and type bigint
        ALTER TABLE order_control ADD COLUMN order_id_tmp BIGINT;
        UPDATE order_control SET order_id_tmp = order_id;

        -- Step 3: Drop the old order_id column of type int
        ALTER TABLE order_control DROP COLUMN order_id;

        -- Step 4: Rename the new column to order_id
        ALTER TABLE order_control RENAME COLUMN order_id_tmp TO order_id;

        RAISE NOTICE 'Column order_id has been successfully updated to type bigint.';
    END IF;
END $$;