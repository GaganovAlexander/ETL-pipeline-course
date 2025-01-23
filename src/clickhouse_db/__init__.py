from re import search

from clickhouse_connect import Client

from configs import CLICKHOUSE_URL, CLICKHOUSE_PORT, CLICKHOUSE_DB, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD


client = Client(
    host=CLICKHOUSE_URL,  
    port=CLICKHOUSE_PORT,         
    username=CLICKHOUSE_USER,
    password=CLICKHOUSE_PASSWORD,       
    database=CLICKHOUSE_DB
)

exist_tables = client.query('SHOW TABLES;').result_columns
table_name_search = r"CREATE TABLE\s+([a-zA-Z0-9_]+)"

with open('./src/clickhouse_db/sql_scripts/clickhouse_db_dump.sql') as init_script:
    for query in init_script.read().split(';'):
        if query.strip() and not search(table_name_search, query).group(1) in exist_tables[0]:
            result = client.command(query)
