import os
import sys
sys.path.append('/opt/airflow')
sys.path.append('/opt/airflow/collect_data')


from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import Variable
from collect_data.api_calls.api_repos import collect_api_repos
from collect_data.dbkit import queries
from typing import Dict, List
import re
import csv
from datetime import datetime



HEADERS = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {Variable.get("github_api_key")}',
    'X-GitHub-Api-Version': '2022-11-28'
}

ORGS = ['moloco', 'woowabros', 'daangn', 'toss',
        'ncsoft', 'line', 'kakao', 'naver', 'nhn']

LICENSES = [
    'agpl-3.0', 'apache-2.0', 'bsd-2-clause', 'bsd-3-clause', 'bsl-1.0', 'cc0-1.0', 'epl-2.0', 'gpl-2.0',
    'gpl-3.0', 'lgpl-2.1', 'mit', 'mpl-2.0', 'unlicense'
]


def collect_repos_data(headers: Dict, orgs: List, execution_date, **kwargs) -> List[tuple]:
    data = collect_api_repos(headers, orgs, execution_date) # <- 이렇게 동작하도록 데코레이터 써서 코드 수정할 것
    sql_name = "API_REPOS_TABLE_INSERT_SQL"

    kwargs['ti'].xcom_push(key='data', value=data)
    kwargs['ti'].xcom_push(key='sql_name', value=sql_name)


def write_to_csv(api_name: str, execution_date, **kwargs):
    data = kwargs['ti'].xcom_pull(key='data')
    sql_name = kwargs['ti'].xcom_pull(key='sql_name')

    year = execution_date.strftime("%Y")
    month = execution_date.strftime("%m")
    day = execution_date.strftime("%d")

    ### sql_name 이용해서 해당 query split
    query = getattr(queries, sql_name)

    # 정규표현식
    matches = re.search(r"\(([^)]+)\)", query)

    ### csv header 처리 ['a', 'b', ... 'd']
    fieldnames = [column.strip() for column in matches.group(1).split(",")]
    fieldnames = [name for name in fieldnames if name]  # 빈 문자열 제거

    filepath = f'/opt/airflow/data/{year}/{month}/{day}/{api_name}.csv'

    # dir 경로 추출
    directory = os.path.dirname(filepath)

    # dir 존재하지 않을 경우 생성
    if not os.path.exists(directory):
        os.makedirs(directory)

    # csv data dir에 저장
    with open(filepath, 'w') as output_file:
        csv_writer = csv.writer(output_file, fieldnames, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        csv_writer.writerow(fieldnames)
        csv_writer.writerows(data) # [(), ()]

    kwargs['ti'].xcom_push(key='filepath', value=filepath)


def upload_to_s3(bucket_name: str, **kwargs) -> None:
    filepath = kwargs['ti'].xcom_pull(key='filepath')
    base_path = '/opt/airflow/'
    s3_key = os.path.relpath(filepath, base_path)

    hook = S3Hook('s3_conn')
    hook.load_file(filename=filepath, key=s3_key, bucket_name=bucket_name)
    os.remove(filepath) # 멱등성 위해 파일 삭제


default_args = {
    'owner': 'airflow',
    'headers': HEADERS,
    'orgs': ORGS,
    'bucket_name': 'ostracker'
}

with DAG(
    'collect_data_and_upload_to_s3',
    default_args=default_args,
    schedule_interval = '0 1 * * *',
    start_date = datetime(2022, 1, 1),
    catchup = False
) as dag:

    collect_repos_data = PythonOperator(
        task_id = 'collect_repos_data',
        python_callable=collect_repos_data,
        provide_context=True,
        op_kwargs = {'headers': HEADERS, 'orgs': ORGS},
    )

    write_repos_to_csv = PythonOperator(
        task_id = 'write_repos_to_csv',
        python_callable=write_to_csv,
        op_kwargs={'api_name': 'repos'},
        provide_context=True,
    )

    upload_repos_csv = PythonOperator(
        task_id = 'upload_repos_csv',
        python_callable=upload_to_s3,
        op_args=['ostracker'],
    )

    collect_repos_data >> write_repos_to_csv >> upload_repos_csv
