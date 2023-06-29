from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from datetime import datetime
from typing import List

from dotenv import load_dotenv
import os

load_dotenv()

# TODO:
#   1. Remove dotenv dependency and use variables.json
#   2. Use SQL provider: https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/index.html

def execute_sqls(sqls: List[str]):
    import psycopg2
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER_NAME'),
        password=os.environ.get('DB_USER_PASSWORD'),
        port=os.environ.get('DB_PORT')
    )

    cursor = conn.cursor()
    for line in sqls:
        cursor.execute(line)
    conn.commit()
    cursor.close()
    conn.close()

@task()
def create_licenses_per_repos_table():
    """
    adhoc 스키마의 테이블에 기반하여 analytics.licenses_per_repos 테이블을 만듭니다.
    """
    from collect_data.dbkit import queries
    execute_sqls([
        queries.ELT_LICENSES_PER_REPOS_TABLE_CREATE_SQL,
        queries.ELT_LICENSES_PER_REPOS_TABLE_INSERT_SQL,
    ])

@dag(
    start_date=datetime(2023, 6, 29),
)
def elt_to_analytics():
    begin = EmptyOperator(task_id="begin")
    end = EmptyOperator(task_id="end")
    
    begin >> [
        create_licenses_per_repos_table()
    ] >> end

elt_to_analytics()

if __name__ == "__main__":
    elt_to_analytics().test()
