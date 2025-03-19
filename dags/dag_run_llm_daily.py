from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'run_llm_daily',
    default_args=default_args,
    description='Run llm script daily',
    schedule_interval='05 13 * * *',  # Cron schedule for 9 PM GMT +8 daily
    start_date=days_ago(1),
    catchup=False,
) as dag:
    
    run_llm = BashOperator(
        task_id='execute_run_llm',
        bash_command='/opt/bitnami/airflow/venv/bin/python /app/run_llm.py',
    )
    
    run_llm