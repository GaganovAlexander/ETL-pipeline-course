import psycopg2 as pg

from configs import POSTGRES_URL, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD


conn = pg.connect(
        host=POSTGRES_URL,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

cur = conn.cursor()