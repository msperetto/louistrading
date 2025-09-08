-- Remoção de tabelas e sequências existentes para reinicializar o banco de dados

-- Remove FKs:


-- Deleta tabelas.
DROP TABLE IF EXISTS public.optmization_tests CASCADE;
DROP TABLE IF EXISTS public.optimization_tests CASCADE;


-- Deleta sequences.

