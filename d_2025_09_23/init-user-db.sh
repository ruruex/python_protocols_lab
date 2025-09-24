#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username postgres <<EOSQL
CREATE USER qytangdbuser;
CREATE DATABASE qytangdb;
GRANT ALL PRIVILEGES ON DATABASE qytangdb TO qytangdbuser;
ALTER USER qytangdbuser WITH PASSWORD 'Cisco0123';
EOSQL
