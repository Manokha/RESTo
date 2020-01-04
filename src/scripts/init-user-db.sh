#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER resto WITH PASSWORD 'resto';
    CREATE DATABASE "resto"
        WITH OWNER "resto"
        ENCODING 'UTF8'
        LC_COLLATE = 'en_US.UTF-8'
        LC_CTYPE = 'en_US.UTF-8'
        TEMPLATE template0;
EOSQL

psql -v ON_ERROR_STOP=1 --username "resto" --dbname "resto" <<-EOSQL
    CREATE TABLE Restaurants (
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL UNIQUE
    );
EOSQL
