-- Altering table public.optmization_tests to add column side (long or short):
ALTER TABLE public.optmization_tests
ADD COLUMN IF NOT EXISTS side VARCHAR(5);