from typing import Dict, List
from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

@task()
def load_from_s3(api_name: str) -> List[Dict]:
    import boto3
    import logging
    import io
    import csv
    import os
    s3 = boto3.client('s3',
        region_name=os.getenv('AWS_REGION_NAME'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )
    response = s3.get_object(Bucket=os.getenv('AWS_S3_BUCKET'), Key=get_object_key('repos', datetime.now()))
    input = io.StringIO(response['Body'].read().decode('utf-8'), newline='')
    reader = csv.reader(input, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    next(reader) # skip header
    result = [row for row in reader]
    logging.info(f'loaded {len(result)} rows for repos')
    return result

@task()
def save_to_rds(data: List[Dict], query: str):
    import psycopg2
    from psycopg2.extras import execute_values
    import os
    import logging
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
    return f'data/{year}/{month}/{day}/{api_name}.csv'

@dag(
    dag_id='s3_to_rds',
    schedule='@daily',
    start_date=datetime(2023, 6, 25, hour=0, minute=0),
    default_args={'retries': 1},
)
def load_csv_from_s3_to_rds():
    begin = EmptyOperator(task_id='begin')
    end = EmptyOperator(task_id='end')

    with TaskGroup('licenses') as licenses:
        from collect_data.dbkit.queries import API_LICENSES_TABLE_INSERT_SQL
        @task()
        def deal_with_licenses(data: List[Dict]):
            return data

        save_to_rds(deal_with_licenses(load_from_s3('licenses')), API_LICENSES_TABLE_INSERT_SQL)

    with TaskGroup('orgs') as orgs:
        from collect_data.dbkit.queries import API_ORGS_TABLE_INSERT_SQL

        @task()
        def deal_with_orgs(data: List[Dict]):
            return data

        save_to_rds(deal_with_orgs(load_from_s3('orgs')), API_ORGS_TABLE_INSERT_SQL)

    with TaskGroup('repos') as repos:
        from collect_data.dbkit.queries import API_REPOS_TABLE_INSERT_SQL
        @task()
        def deal_with_repos(data: List[Dict]):
            return data

        save_to_rds(deal_with_repos(load_from_s3('repos')), API_REPOS_TABLE_INSERT_SQL)

    with TaskGroup('repos_commits') as repos_commits:
        from collect_data.dbkit.queries import API_REPOS_COMMITS_TABLE_INSERT_SQL
        @task()
        def deal_with_repos_commits(data: List[Dict]):
            return data

        save_to_rds(deal_with_repos_commits(load_from_s3('repos_commits')), API_REPOS_COMMITS_TABLE_INSERT_SQL)

    with TaskGroup('repos_issues') as repos_issues:
        from collect_data.dbkit.queries import API_REPOS_ISSUES_TABLE_INSERT_SQL
        @task()
        def deal_with_repos_issues(data: List[Dict]):
            return data

        save_to_rds(deal_with_repos_issues(load_from_s3('repos_issues')), API_REPOS_ISSUES_TABLE_INSERT_SQL)


    with TaskGroup('repos_languages') as repos_languages:
        from collect_data.dbkit.queries import API_REPOS_LANGUAGES_TABLE_INSERT_SQL
        @task()
        def deal_with_repos_languages(data: List[Dict]):
            return data

        save_to_rds(deal_with_repos_languages(load_from_s3('repos_languages')), API_REPOS_LANGUAGES_TABLE_INSERT_SQL)

        
    with TaskGroup('repos_licenses') as repos_licenses:
        from collect_data.dbkit.queries import API_REPOS_LICENSES_TABLE_INSERT_SQL
        @task()
        def deal_with_repos_licenses(data: List[Dict]):
            return data

        save_to_rds(deal_with_repos_licenses(load_from_s3('repos_licenses')), API_REPOS_LICENSES_TABLE_INSERT_SQL)

    begin >> [
        licenses, orgs, repos, repos_commits, repos_issues, repos_languages, repos_licenses
    ] >> end

load_csv_from_s3_to_rds()

if __name__ == '__main__':
    # test dag
    # https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/debug.html
    load_csv_from_s3_to_rds().test()
