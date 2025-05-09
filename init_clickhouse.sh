#!/bin/bash

set -a
source .env
set +a

curl -u "$CLICKHOUSE_USER:$CLICKHOUSE_PASSWORD" \
  -X POST "http://127.0.0.1:${CLICKHOUSE_PORT}" \
  -d "CREATE DATABASE IF NOT EXISTS ${CLICKHOUSE_DB};"
