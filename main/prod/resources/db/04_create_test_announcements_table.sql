-- Create table for fake delist announcements for testing
CREATE TABLE IF NOT EXISTS public.test_delist_announcement (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    announcement_date VARCHAR(10) NOT NULL,
    coins TEXT[] NOT NULL, -- Array of coin symbols
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    notes TEXT
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_test_delist_announcement_processed ON public.test_delist_announcement(processed);
CREATE INDEX IF NOT EXISTS idx_test_delist_announcement_date ON public.test_delist_announcement(announcement_date);
