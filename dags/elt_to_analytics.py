from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()

# TODO:
#   1. Remove dotenv dependency and use variables.json
#   2. Use SQL provider: https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/index.html

def connect_database():
    import psycopg2
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER_NAME'),
        password=os.environ.get('DB_USER_PASSWORD'),
        port=os.environ.get('DB_PORT')
    )
    return conn

@task()
def create_licenses_per_repos_table():
    """
    adhoc 스키마의 테이블에 기반하여 analytics.licenses_per_repos 테이블을 만듭니다.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
    DROP TABLE IF EXISTS analytics.licenses_per_repos;
    CREATE TABLE analytics.licenses_per_repos (
        repo VARCHAR(255),
        organization VARCHAR(255),
        name VARCHAR(255),
        spdx_id VARCHAR(40)
    );
    INSERT INTO analytics.licenses_per_repos (repo, organization, name, spdx_id)
    SELECT
      DISTINCT repos.full_name as repo,
      orgs.name as organization,
      ls.name,
      ls.spdx_id
    FROM adhoc.api_repos repos
    JOIN (
      SELECT orgs_id, name FROM adhoc.api_orgs WHERE called_at = (SELECT called_at FROM adhoc.api_orgs ORDER BY 1 DESC LIMIT 1)
    ) orgs ON repos.owner_id = orgs.orgs_id
    JOIN (
      SELECT repo_full_name, license_key FROM adhoc.api_repos_licenses WHERE called_at = (SELECT called_at FROM adhoc.api_repos_licenses ORDER BY 1 DESC LIMIT 1)
    ) rl ON repos.full_name = rl.repo_full_name
    JOIN (
      SELECT key, name, spdx_id FROM adhoc.api_licenses WHERE called_at = (SELECT called_at FROM adhoc.api_licenses ORDER BY 1 DESC LIMIT 1)
    ) ls ON ls.key = rl.license_key
    WHERE repos.called_at = (SELECT called_at FROM adhoc.api_repos ORDER BY 1 DESC LIMIT 1)
    ORDER BY 2;
    """)
    conn.commit()
    cursor.close()
    conn.close()

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
