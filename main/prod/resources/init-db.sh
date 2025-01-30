#!/bin/bash
set -e

# Wait for PostgreSQL to start
until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done

echo "Postgres is up - executing command"

# Check if the table 'initial_config' exists
if psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\dt' | grep -q 'initial_config'; then
  echo "Database already initialized"
else
  # Run the SQL script to initialize the database
  psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -a -f /resources/01_create_tables.sql
  psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -a -f /resources/02_insert_data.sql
fi

exec "$@"