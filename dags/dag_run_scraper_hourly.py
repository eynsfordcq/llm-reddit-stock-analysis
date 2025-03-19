from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'run_scraper_hourly',
    default_args=default_args,
    description='Run scraper script every hour',
    schedule_interval='@hourly',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    run_scraper = BashOperator(
        task_id='execute_run_scraper',
        bash_command='/opt/bitnami/airflow/venv/bin/python /app/run_scraper.py',
    )

    run_scraper