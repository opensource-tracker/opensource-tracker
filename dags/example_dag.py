from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'nyeong',
    'start_date': datetime(2023, 6, 25, hour=0, minute=0),
    'email': ['me@annyeong.me'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dag_v1',
    schedule='0 9 * * *',
    tags=['test'],
    catchup=False,
    default_args=default_args
)

start = BashOperator(
    dag=dag,
    task_id='print_date',
    bash_command='date',
)

t1 = BashOperator(
    dag=dag,
    task_id='sleep',
    bash_command='sleep 5',
)

t2 = BashOperator(
    dag=dag,
    task_id='ls',
    bash_command='ls /tmp',
)

end = BashOperator(
    dag=dag,
    bash_command='echo end',
    task_id='echo'
)

start >> [t1, t2] >> end
