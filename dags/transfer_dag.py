from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src import transfer


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
}
with DAG(
    'transfer_dag',
    default_args=default_args,
    description='DAG для извлечения данных из postgres, их трансформации и загрузки в clickhouse',
    schedule_interval=None,
    catchup=False,
) as dag:
    transfer_products_task = PythonOperator(
        task_id='transfer_products',
        python_callable=transfer.transfer_products,
    )
    transfer_orders_task = PythonOperator(
        task_id='transfer_orders',
        python_callable=transfer.transfer_orders,
    )
    transfer_payments_task = PythonOperator(
        task_id='transfer_payments',
        python_callable=transfer.transfer_payments,
    )
    transfer_reviews_task = PythonOperator(
        task_id='transfer_reviews',
        python_callable=transfer.transfer_reviews,
    )
    transfer_change_logs_task = PythonOperator(
        task_id='transfer_change_logs',
        python_callable=transfer.transfer_change_logs,
    )
    