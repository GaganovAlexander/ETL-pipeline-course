import psycopg2 as pg

from src.configs import POSTGRES_URL, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, WORKING_DIR


conn = pg.connect(
        host=POSTGRES_URL,
        port=5432,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

cur = conn.cursor()

with open(WORKING_DIR + '/src/postgres_db/sql_scripts/postgres_db_dump.sql') as sql_dump:
    commands = sql_dump.read().split(';')
    for command in commands:
        command = command.strip()
        if command:
            cur.execute(command)
    conn.commit()