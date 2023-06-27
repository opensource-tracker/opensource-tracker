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
    # response = s3.get_object(Bucket=os.getenv('AWS_S3_BUCKET'), Key=get_object_key('repos', datetime.now()))
    response = s3.get_object(Bucket=os.getenv('AWS_S3_BUCKET'), Key='test_collect/orgs/2023/06/27/collect.csv')
    input = io.StringIO(response['Body'].read().decode('utf-8'), newline='')
    reader = csv.DictReader(input, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    result = [row for row in reader]
    logging.info(f'loaded {len(result)} rows for repos')
    return result

@task()
def save_to_rds(data: List[Dict], query: str):
    import psycopg2
    import os
    import logging
    db = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER_NAME'),
        password=os.environ.get('DB_USER_PASSWORD'),
        port=os.environ.get('DB_PORT')
    )
    for row in data:
        db.cursor().execute(query, row)
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
        @task()
        def deal_with_licenses(data: List[Dict]):
            return data
        query = """
            INSERT INTO adhoc.api_licenses
            (key, name, spdx_id, node_id, url, body, permissions, conditions, limitations, called_at)
            VALUES
            (%(key)s, %(name)s, %(spdx_id)s, %(node_id)s, %(url)s, %(body)s, %(permissions)s, %(conditions)s, %(limitations)s, %(called_at)s)
        """

        save_to_rds(deal_with_licenses(load_from_s3('licenses')), query)

    with TaskGroup('orgs') as orgs:
        @task()
        def deal_with_orgs(data: List[Dict]):
            return data
        query = """
            INSERT INTO adhoc.api_orgs
            (orgs_id, node_id, name, description, company, blog, location, email, twitter_username,
            followers, following, is_verified, has_organization_projects, has_repository_projects,
            public_repos, public_gists, html_url, avatar_url, type, created_at, updated_at, called_at)
            VALUES 
            (%(id)s, %(node_id)s, %(name)s, %(description)s, %(company)s, %(blog)s, %(location)s, %(email)s,
            %(twitter_username)s, %(followers)s, %(following)s, %(is_verified)s, %(has_organization_projects)s,
            %(has_repository_projects)s, %(public_repos)s, %(public_gists)s, %(html_url)s, %(avatar_url)s, %(type)s,
            %(created_at)s, %(updated_at)s, %(current_time)s)
        """

        save_to_rds(deal_with_orgs(load_from_s3('orgs')), query)

    with TaskGroup('repos') as repos:
        @task()
        def deal_with_repos(data: List[Dict]):
            return data
        query = """
                INSERT INTO adhoc.api_repos
                (repo_id, node_id, owner_id, name, full_name, description, private, html_url,
                url, homepage, fork, created_at, updated_at, pushed_at, called_at, size, stargazers_count, forks_count,
                open_issues_count, language, archived, disabled, license, allow_forking)
                VALUES
                (%(repo_id)s, %(node_id)s, %(owner_id)s, %(name)s, %(full_name)s, %(description)s, %(private)s,
                %(html_url)s, %(url)s, %(homepage)s, %(fork)s, %(created_at)s, %(updated_at)s, %(pushed_at)s,
                %(called_at)s, %(size)s, %(stargazers_count)s, %(forks_count)s, %(open_issues_count)s, %(language)s,
                %(archived)s, %(disabled)s, %(license)s, %(allow_forking)s)
                """

        save_to_rds(deal_with_repos(load_from_s3('repos')), query)

    with TaskGroup('repos_commits') as repos_commits:
        @task()
        def deal_with_repos_commits(data: List[Dict]):
            return data
        query = """
                INSERT INTO adhoc.api_repos_commits 
                (sha, node_id, commit_author_name, commit_author_email, commit_author_date,
                commit_committer_name, commit_committer_email, commit_committer_date,
                commit_message, author_login, author_id, author_node_id, author_site_admin,
                committer_login, committer_id, committer_node_id, committer_site_admin,
                repo_full_name, called_at)
                VALUES  
                (%(sha)s, %(node_id)s, %(commit_author_name)s, %(commit_author_email)s, %(commit_author_date)s,
                %(commit_committer_name)s, %(commit_committer_email)s, %(commit_committer_date)s,
                %(commit_message)s, %(author_login)s, %(author_id)s, %(author_node_id)s, %(author_site_admin)s,
                %(committer_login)s, %(committer_id)s, %(committer_node_id)s, %(committer_site_admin)s,
                %(repo_full_name)s, %(called_at)s)
                """

        save_to_rds(deal_with_repos_commits(load_from_s3('repos_commits')), query)

    with TaskGroup('repos_issues') as repos_issues:
        @task()
        def deal_with_repos_issues(data: List[Dict]):
            return data
        query = """
                INSERT INTO adhoc.api_repos_issues
                (repository_url, labels_url, comments_url, events_url, html_url, issues_id, node_id, number, title, state, locked,
                comments, created_at, updated_at, author_association, body, timeline_url, state_reason, login_user, called_at,
                repo_full_name)
                VALUES  
                (%(repository_url)s,%(labels_url)s,%(comments_url)s,%(events_url)s,%(html_url)s,%(issues_id)s,%(node_id)s,%(number)s,%(title)s,%(state)s,%(locked)s,
                %(comments)s,%(created_at)s,%(updated_at)s,%(author_association)s,%(body)s,%(timeline_url)s,%(state_reason)s,%(login_user)s,%(called_at)s,
                %(repo_full_name)s)
                """

        save_to_rds(deal_with_repos_issues(load_from_s3('repos_issues')), query)


    with TaskGroup('repos_languages') as repos_languages:
        @task()
        def deal_with_repos_languages(data: List[Dict]):
            return data
        query = """
                INSERT INTO adhoc.api_repos_languages (repo_full_name, language, usage_count, called_at)
                VALUES  
                (%(repo_full_name)s, %(language)s, %(usage_count)s, %(called_at)s)
                """

        save_to_rds(deal_with_repos_languages(load_from_s3('repos_languages')), query) 

        
    with TaskGroup('repos_licenses') as repos_licenses:
        @task()
        def deal_with_repos_licenses(data: List[Dict]):
            return data
        query = """
                INSERT INTO adhoc.api_repos_licenses
                (repo_full_name, license_key, sha, html_url, download_url, git_url, content, called_at)
                VALUES  
                (%(repo_full_name)s, %(license_key)s, %(sha)s, %(html_url)s, %(download_url)s, %(git_url)s, %(content)s, %(called_at)s)
                """

        save_to_rds(deal_with_repos_licenses(load_from_s3('repos_licenses')), query)    

    begin >> [
        licenses, orgs, repos, repos_commits, repos_issues, repos_languages, repos_licenses
    ] >> end

load_csv_from_s3_to_rds()

if __name__ == '__main__':
    # test dag
    # https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/debug.html
    load_csv_from_s3_to_rds().test()
