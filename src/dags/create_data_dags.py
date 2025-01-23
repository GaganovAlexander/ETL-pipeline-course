from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import psycopg2

# Подключение к базе данных
def get_conn_and_cursor():
    conn = psycopg2.connect(
        dbname="your_db",
        user="your_user",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    cur = conn.cursor()
    return conn, cur

# Функции из вашего кода
def roles_task(**kwargs):
    conn, cur = get_conn_and_cursor()
    roles(conn, cur)
    conn.close()

def users_task(**kwargs):
    conn, cur = get_conn_and_cursor()
    generic = kwargs['ti'].xcom_pull(task_ids='init_generic')
    users(conn, cur, generic)
    conn.close()