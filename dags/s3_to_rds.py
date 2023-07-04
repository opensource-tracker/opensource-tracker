from typing import Dict, List
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import execute_values
from datetime import datetime
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

def load_from_s3(s3_key: str) -> List[List]:
    """
    s3_key를 받아 S3에서 데이터를 불러옵니다.
    """
    import logging
    import csv
    import io
    hook = S3Hook('s3_conn')
    content = hook.read_key(key=s3_key, bucket_name=Variable.get('AWS_S3_BUCKET'))
    input = io.StringIO(content, newline='')
    reader = csv.reader(input, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    next(reader) # skip header
    result = []
    for row in reader:
        row = [cell if cell else None for cell in row]
        result.append(row)

    logging.info(f'loaded {len(result)} rows for repos')
    return result

def save_to_rds(data: List[Dict], query: str):
    import logging
    hook = PostgresHook('ostracker_conn')
    conn = hook.get_conn()
    cursor = conn.cursor()
    execute_values(cursor, query, data)
    conn.commit()
    logging.info(f'saved {len(data)} rows for repos into rds')

def get_object_key(api_name: str, date: datetime) -> str:
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    return f'data/year={year}/month={month}/day={day}/{api_name}.csv'

@dag(
    dag_id='s3_to_rds',
    start_date=datetime(2023, 6, 25, hour=0, minute=0),
    default_args={'retries': 0},
    catchup=False
)
def load_to_rds():
    """
    S3에 적재한 /year={yyyy}/month={mm}/day={dd}/api.csv` 형식의 파일을 RDS에 적재합니다.
    """
    begin = EmptyOperator(task_id='begin')
    elt_to_analytics = TriggerDagRunOperator(
        task_id='trigger_elt_to_analytics',
        trigger_dag_id='elt_to_analytics',
    )
    from collect_data.dbkit import queries

    begin >> [
        task_for(api_name='licenses', query=queries.API_LICENSES_TABLE_INSERT_SQL),
        task_for(api_name='orgs', query=queries.API_ORGS_TABLE_INSERT_SQL),
        task_for(api_name='repos', query=queries.API_REPOS_TABLE_INSERT_SQL),
        task_for(api_name='repos_commits', query=queries.API_REPOS_COMMITS_TABLE_INSERT_SQL),
        task_for(api_name='repos_issues', query=queries.API_REPOS_ISSUES_TABLE_INSERT_SQL),
        task_for(api_name='repos_languages', query=queries.API_REPOS_LANGUAGES_TABLE_INSERT_SQL),
        task_for(api_name='repos_licenses', query=queries.API_REPOS_LICENSES_TABLE_INSERT_SQL),
    ] >> elt_to_analytics

def task_for(api_name: str, query: str):
    @task(task_id=f'task_{api_name}')
    def _task_for(api_name: str, query: str, **kwargs):
        execution_date = kwargs['execution_date']
        s3_key = get_object_key(api_name, execution_date)
        data = load_from_s3(s3_key)
        save_to_rds(data, query)
    return _task_for(api_name, query)

load_to_rds()

if __name__ == '__main__':
    # test dag
    # https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/debug.html
    load_to_rds().test()
