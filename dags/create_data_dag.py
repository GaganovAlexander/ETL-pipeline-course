from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.postgres_db import create_data


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
}
with DAG(
    'create_data_dag',
    default_args=default_args,
    description='DAG для создания искусственных данных',
    schedule_interval=None,
    catchup=False,
) as dag:
    roles_task = PythonOperator(
        task_id='roles',
        python_callable=create_data.roles,
    )

    users_task = PythonOperator(
        task_id='users',
        python_callable=create_data.users,
    )

    categories_task = PythonOperator(
        task_id='categories',
        python_callable=create_data.categories,
    )

    products_task = PythonOperator(
        task_id='products',
        python_callable=create_data.products,
    )

    pick_up_points_task = PythonOperator(
        task_id='pick_up_points',
        python_callable=create_data.pick_up_points,
    )

    order_statuses_task = PythonOperator(
        task_id='order_statuses',
        python_callable=create_data.order_statuses,
    )

    orders_task = PythonOperator(
        task_id='orders',
        python_callable=create_data.orders,
    )

    order_items_task = PythonOperator(
        task_id='order_items',
        python_callable=create_data.order_items,
    )

    payment_statuses_task = PythonOperator(
        task_id='payments_statuses',
        python_callable=create_data.payments_statuses,
    )

    payment_methods_task = PythonOperator(
        task_id='payments_methods',
        python_callable=create_data.payments_methods,
    )

    payments_task = PythonOperator(
        task_id='payments',
        python_callable=create_data.payments,
    )

    reviews_task = PythonOperator(
        task_id='reviews',
        python_callable=create_data.reviews,
    )

    review_attachments_task = PythonOperator(
        task_id='review_attachments',
        python_callable=create_data.review_attachments,
    )

    change_logs_task = PythonOperator(
        task_id='change_logs',
        python_callable=create_data.change_logs,
    )

    roles_task >> users_task >> [orders_task, order_items_task, reviews_task, change_logs_task]
    categories_task >> products_task >> [order_items_task, reviews_task]
    [pick_up_points_task, order_statuses_task] >> orders_task
    orders_task >> [order_items_task, payments_task]
    [payment_statuses_task, payment_methods_task] >> payments_task
    reviews_task >> review_attachments_task