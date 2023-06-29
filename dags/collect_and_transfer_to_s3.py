from collect_data.dbkit import queries
from collect_data.api_calls.api_repos_languages import collect_api_repos_languages
from collect_data.api_calls.api_repos_licenses import collect_api_repos_licenses
from collect_data.api_calls.api_repos_issues import collect_api_repos_issues
from collect_data.api_calls.api_repos_commits import collect_api_repos_commits
from collect_data.api_calls.api_orgs import collect_api_orgs
from collect_data.api_calls.api_repos import collect_api_repos
from airflow.operators.empty import EmptyOperator
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from typing import Dict, List
from datetime import datetime
import csv
import re
from io import StringIO, BytesIO


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

api_keyword = {
    'repos': [collect_api_repos, "API_REPOS_TABLE_INSERT_SQL"],
    'orgs': [collect_api_orgs, "API_ORGS_TABLE_INSERT_SQL"],
    # 'licenses': [],
    'repos_commits': [collect_api_repos_commits, "API_REPOS_COMMITS_TABLE_INSERT_SQL"],
    'repos_issues': [collect_api_repos_issues, "API_REPOS_ISSUES_TABLE_INSERT_SQL"],
    'repos_licenses': [collect_api_repos_licenses, "API_REPOS_LICENSES_TABLE_INSERT_SQL"],
    'repos_languages': [collect_api_repos_languages, "API_REPOS_LANGUAGES_TABLE_INSERT_SQL"],
}


def collect_data(api_name: str, headers: Dict, val: List, execution_date) -> List[tuple]:
    data = api_keyword[api_name][0](headers, val, execution_date)
    return data


def get_file_path(api_name: str, execution_date):
    year = execution_date.strftime("%Y")
    month = execution_date.strftime("%m")
    day = execution_date.strftime("%d")

    return f'data/year={year}/month={month}/day={day}/{api_name}.csv'


def write_to_csv(api_name: str, data: List[tuple]):
    sql_name = api_keyword[api_name][1]

    # sql_name 이용해서 해당 query split
    query = getattr(queries, sql_name)

    # 정규표현식
    matches = re.search(r"\(([^)]+)\)", query)

    # csv header 처리 ['a', 'b', ... 'd']
    fieldnames = [column.strip() for column in matches.group(1).split(",")]
    fieldnames = [name for name in fieldnames if name]  # 빈 문자열 제거

    # csv data buffer에 저장

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer, fieldnames, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    csv_writer.writerow(fieldnames)
    csv_writer.writerows(data)

    csv_byte_buffer = BytesIO(csv_buffer.getvalue().encode())
    return csv_byte_buffer


def upload_to_s3(bucket_name, s3_key: str, csv_buffer) -> None:
    hook = S3Hook('s3_conn')
    hook.load_file_obj(file_obj=csv_buffer, key=s3_key, bucket_name=bucket_name, replace=True)


def get_repos_full_name_from_s3(bucket_name, s3_key):
    input_serialization = {
    'CSV': {
        'FileHeaderInfo': 'USE',
        'RecordDelimiter': '\n',
        'FieldDelimiter': ',',
        'Comments': '#',
        }
    }
    s3_key = '/'.join(s3_key.split('/')[:-1]) + '/repos.csv'
    hook = S3Hook('s3_conn')

    s3_file = hook.select_key(
        s3_key, bucket_name=bucket_name, expression='SELECT "full_name" FROM S3Object', input_serialization=input_serialization)

    return s3_file.rstrip().split('\n')


def create_task(api_name):
    @task(task_id=f'task_{api_name}')
    def task_for(api_name: str, **kwargs):
        execution_date = kwargs['execution_date']
        bucket_name = Variable.get('AWS_S3_BUCKET')
        headers = HEADERS
        orgs = ORGS
        s3_key = get_file_path(api_name, execution_date)

        if api_name in ['repos_issues', 'repos_commits', 'repos_licenses', 'repos_languages']:
            repos = get_repos_full_name_from_s3(bucket_name, s3_key)
            data = collect_data(api_name, headers, repos, execution_date)
        else:
            data = collect_data(api_name, headers, orgs, execution_date)

        csv_buffer = write_to_csv(api_name, data)
        upload_to_s3(bucket_name, s3_key, csv_buffer)
    return task_for(api_name)


@dag(
    schedule='0 1 * * *',
    start_date=datetime(2023, 6, 25),
    default_args={
        'owner': 'airflow',
        'headers': HEADERS,
        'orgs': ORGS,
    },
    catchup=False,
)
def extract_data_and_save_csv_to_s3():
    begin = EmptyOperator(task_id='begin')
    s3_to_rds = TriggerDagRunOperator(
        task_id='trigger_s3_to_rds',
        trigger_dag_id='s3_to_rds',
    )

    begin >> create_task('repos') >> [create_task(api_name) for api_name in api_keyword.keys() if api_name != 'repos'] >> s3_to_rds

extract_data_and_save_csv_to_s3()
