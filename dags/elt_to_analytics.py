from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
from typing import List
from collect_data.dbkit import queries


# TODO:
#   1. Remove dotenv dependency and use variables.json
#   2. Use SQL provider: https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/index.html

def execute_sqls(sqls: List[str]):
    hook = PostgresHook('ostracker_conn')
    conn = hook.get_conn()
    cursor = conn.cursor()
    for line in sqls:
        cursor.execute(line)
    conn.commit()
    cursor.close()
    conn.close()

@task()
def create_licenses_per_repos_table():
    """
    raw_data 스키마의 테이블에 기반하여 analytics.licenses_per_repos 테이블을 만듭니다.
    """
    execute_sqls([
        queries.ELT_LICENSES_PER_REPOS_TABLE_CREATE_SQL,
        queries.ELT_LICENSES_PER_REPOS_TABLE_INSERT_SQL,
    ])

@task()
def create_recent_repos_table():
    """
    raw_data 스키마의 테이블에 기반하여 analytics.recent_repos 테이블을 만듭니다.
    """
    execute_sqls([
        queries.ELT_RECENT_REPOS_TABLE_CREATE_SQL,
        queries.ELT_RECENT_REPOS_TABLE_INSESRT_SQL,
    ])

@task()
def create_languages_per_repos_table():
    execute_sqls([
        queries.ELT_LANGUAGES_PER_REPOS_TABLE_CREATE_SQL,
        queries.ELT_LANGUAGES_PER_REPOS_TABLE_INSERT_SQL
    ])


@dag(
    start_date=datetime(2023, 6, 29),
    catchup=False
)
def elt_to_analytics():
    begin = EmptyOperator(task_id="begin")
    end = EmptyOperator(task_id="end")

    begin >> [
        create_licenses_per_repos_table(),
        create_recent_repos_table(),
        create_languages_per_repos_table()
    ] >> end

elt_to_analytics()

if __name__ == "__main__":
    elt_to_analytics().test()
