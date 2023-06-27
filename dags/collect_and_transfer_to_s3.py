import csv
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import Variable
from collect_data.api_calls.api_repos import collect_api_repos
from typing import Dict, List
import os

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

@task
def collect_repo_data(headers: Dict, orgs: List, current_time) -> List[Dict]:
    return collect_api_repos(headers, orgs, current_time)


def write_to_csv(data: List[Dict], filename: str):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def upload_to_s3(filename: str, key: str, bucket_name: str) -> None:
    hook = S3Hook('s3_conn')
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)
    os.remove(filename)


def github_to_s3():
    headers = Variable.get("github_headers", deserialize_json=True)
    orgs = Variable.get("github_orgs", deserialize_json=True)
    current_time = datetime.now()

    data = collect_api_repos(headers, orgs, current_time)
    filename = "/path/to/your/file.csv"  # update with your file path
    write_to_csv(data, filename)

    bucket_name = "your_bucket_name"  # update with your bucket name
    object_name = "collect/data/file.csv"  # update with your object name
    upload_to_s3(filename, bucket_name, object_name)


with DAG(
    'collect_data_and_upload_to_s3',
    schedule_interval = timedelta(minutes=5),
    start_date = datetime(2022, 1, 1),
    catchup = False
) as dag:

    upload = PythonOperator(
        task_id = 'upload',
        python_callable = upload_to_s3,
        op_kwargs = {
            'filename' : '/opt/airflow/data/employee_test.csv',
            'key' : 'data/employee.csv',
            'bucket_name' : 'mysql-export-data'
        }
    )
