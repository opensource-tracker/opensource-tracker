import datetime
import os
import logging
from api_calls.api_orgs import collect_api_orgs
from api_calls.api_repos_licenses import collect_api_repos_licenses
from api_calls.api_licenses import collect_api_licenses
from api_calls.api_repos_issues import collect_api_repos_issues
from api_calls.api_repos_commits import collect_api_repos_commits
from api_calls.api_repos import collect_api_repos
from api_calls.api_repos_languages import collect_api_repos_languages
from dbkit.db_connector import psqlConnector
from dbkit.queries import API_ORGS_TABLE_INSERT_SQL, API_LICENSES_TABLE_INSERT_SQL, \
    API_REPOS_LICENSES_TABLE_INSERT_SQL, API_REPOS_SELECT_FULL_NAME_SQL, API_REPOS_COMMITS_TABLE_INSERT_SQL, \
    API_REPOS_TABLE_INSERT_SQL, API_REPOS_LANGUAGES_TABLE_INSERT_SQL, API_REPOS_ISSUES_TABLE_INSERT_SQL
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {os.environ.get("API_TOKEN")}',
    'X-GitHub-Api-Version': '2022-11-28'
}

ORGS = ['moloco', 'woowabros', 'daangn', 'toss',
        'ncsoft', 'line', 'kakao', 'naver', 'nhn']

LICENSES = [
    'agpl-3.0', 'apache-2.0', 'bsd-2-clause', 'bsd-3-clause', 'bsl-1.0', 'cc0-1.0', 'epl-2.0', 'gpl-2.0',
    'gpl-3.0', 'lgpl-2.1', 'mit', 'mpl-2.0', 'unlicense'
]


def run():
    db = psqlConnector()
    CURRENT_TIME = datetime.datetime.now()

    print(">>> collect orgs started")
    logging.info(">>> collect orgs started")
    orgs_data = collect_api_orgs(HEADERS, ORGS, CURRENT_TIME)
    db.insert_data(API_ORGS_TABLE_INSERT_SQL, orgs_data)

    print(">>> collect repos started")
    logging.info(">>> collect repos started")
    repos_data = collect_api_repos(HEADERS, ORGS, CURRENT_TIME)
    db.insert_data(API_REPOS_TABLE_INSERT_SQL, repos_data)

    # # repos: [(full_name,), (full_name,), ...]
    repos = db.select_data(API_REPOS_SELECT_FULL_NAME_SQL)
    repos = [repo[0] for repo in repos]

    print(">>> collect repo licenses started")
    logging.info(">>> collect repo licenses started")
    repos_licenses_data = collect_api_repos_licenses(
        HEADERS, repos, CURRENT_TIME)
    db.insert_data(API_REPOS_LICENSES_TABLE_INSERT_SQL, repos_licenses_data)

    print(">>> collect repo commits started")
    logging.info(">>> collect repo commits started")
    repos_commits_data = collect_api_repos_commits(
        HEADERS, repos, CURRENT_TIME)
    for values in repos_commits_data:
        db.insert_data(API_REPOS_COMMITS_TABLE_INSERT_SQL, [values])

    # # # licenses는 데이터 갱신이 필요 없어서 중복된 값은 예외처리 하겠습니다.
    print(">>> collect licenses started")
    logging.info(">>> collect licenses started")
    licenses_data = collect_api_licenses(HEADERS, LICENSES, CURRENT_TIME)
    for values in licenses_data:
        db.insert_data(API_LICENSES_TABLE_INSERT_SQL, [values])

    print(">>> collect issues started")
    logging.info(">>> collect repo issues started")
    issues_data = collect_api_repos_issues(HEADERS, repos, CURRENT_TIME)
    for values in issues_data:
        db.insert_data(API_REPOS_ISSUES_TABLE_INSERT_SQL, [values])

    print(">>> collect repo languages started")
    logging.info(">>> collect repo languages started")
    repos_languages_data = collect_api_repos_languages(
        HEADERS, repos, CURRENT_TIME)
    db.insert_data(API_REPOS_LANGUAGES_TABLE_INSERT_SQL, repos_languages_data)

    db.disconnect()


if __name__ == "__main__":
    run()
