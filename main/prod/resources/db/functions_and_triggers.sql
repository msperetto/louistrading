CREATE OR REPLACE FUNCTION update_last_updated_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_update = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_last_updated_account_balance
BEFORE UPDATE ON account_balance
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_column();