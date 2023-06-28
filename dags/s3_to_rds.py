from typing import Dict, List
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

def load_from_s3(s3_key: str) -> List[List]:
    """
    s3_key를 받아 S3에서 데이터를 불러옵니다.
    """
    import logging
    import boto3
    import csv
    import io
    import os
    s3 = boto3.client('s3',
        region_name=os.getenv('AWS_REGION_NAME'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )
    response = s3.get_object(Bucket=os.getenv('AWS_S3_BUCKET'), Key=s3_key)
    input = io.StringIO(response['Body'].read().decode('utf-8'), newline='')
    reader = csv.reader(input, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    next(reader) # skip header
    result = [row for row in reader]
    logging.info(f'loaded {len(result)} rows for repos')
    return result

def save_to_rds(data: List[Dict], query: str):
    import psycopg2
    import logging
    import os
    from psycopg2.extras import execute_values
    db = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER_NAME'),
        password=os.environ.get('DB_USER_PASSWORD'),
        port=os.environ.get('DB_PORT')
    )
    cursor = db.cursor()
    execute_values(cursor, query, data)
    db.commit()
    logging.info(f'saved {len(data)} rows for repos into rds')

def get_object_key(api_name: str, date: datetime) -> str:
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    return f'data/year={year}/month={month}/day={day}/{api_name}.csv'

@dag(
    dag_id='s3_to_rds',
    schedule='@daily',
    start_date=datetime(2023, 6, 25, hour=0, minute=0),
    default_args={'retries': 1},
)
def load_to_rds():
    """
    S3에 적재한 /year={yyyy}/month={mm}/day={dd}/api.csv` 형식의 파일을 RDS에 적재합니다.
    """
    begin = EmptyOperator(task_id='begin')
    end = EmptyOperator(task_id='end')

    from collect_data.dbkit import queries

    begin >> [
        task_for(api_name='licenses', query=queries.API_LICENSES_TABLE_INSERT_SQL),
        task_for(api_name='orgs', query=queries.API_ORGS_TABLE_INSERT_SQL),
        task_for(api_name='repos', query=queries.API_REPOS_TABLE_INSERT_SQL),
        task_for(api_name='repos_commits', query=queries.API_REPOS_COMMITS_TABLE_INSERT_SQL),
        task_for(api_name='repos_issues', query=queries.API_REPOS_ISSUES_TABLE_INSERT_SQL),
        task_for(api_name='repos_languages', query=queries.API_REPOS_LANGUAGES_TABLE_INSERT_SQL),
        task_for(api_name='repos_licenses', query=queries.API_REPOS_LICENSES_TABLE_INSERT_SQL),
    ] >> end

@task()
def task_for(api_name: str, query: str):
    s3_key = get_object_key(api_name, datetime.now())
    data = load_from_s3(s3_key)
    save_to_rds(data, query)

load_to_rds()

if __name__ == '__main__':
    # test dag
    # https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/debug.html
    load_to_rds().test()
