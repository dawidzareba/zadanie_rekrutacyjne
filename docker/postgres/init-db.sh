#!/bin/bash
set -e

# Create the database user and database if they don't exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO
    \$do\$
    BEGIN
       IF NOT EXISTS (
          SELECT FROM pg_catalog.pg_roles
          WHERE  rolname = '$DB_USER') THEN
          CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS';
       END IF;
    END
    \$do\$;
    
    ALTER ROLE $DB_USER CREATEDB;
    
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL