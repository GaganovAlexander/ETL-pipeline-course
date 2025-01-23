from os import environ

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv(), override=True)

POSTGRES_URL = environ.get("POSTGRES_URL")
POSTGRES_PORT = environ.get("POSTGRES_PORT")
POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_DB = environ.get("POSTGRES_DB")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD", "")

CLICKHOUSE_URL = environ.get("CLICKHOUSE_URL")
CLICKHOUSE_PORT = environ.get("CLICKHOUSE_PORT")
CLICKHOUSE_USER = environ.get("CLICKHOUSE_USER")
CLICKHOUSE_DB = environ.get("CLICKHOUSE_DB")
CLICKHOUSE_PASSWORD = environ.get("CLICKHOUSE_PASSWORD", "")