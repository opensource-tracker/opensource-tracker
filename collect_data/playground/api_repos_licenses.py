"""
adhoc.api_repos_licenses에 API 정보를 적재하는 예시 코드 조각입니다
"""
from dotenv import load_dotenv
from datetime import datetime
import psycopg2
import os
import requests

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    port=os.getenv('DB_PORT'),
    host=os.getenv('DB_HOST'),
)

insert_query = """
INSERT INTO adhoc.api_repos_licenses
(repo_full_name, license_key, sha, html_url, download_url, git_url, content, called_at)
VALUES
(%(repo_full_name)s, %(license_key)s, %(sha)s, %(html_url)s, %(download_url)s, %(git_url)s, %(content)s, %(called_at)s)
"""


github_token = os.getenv('GITHUB_TOKEN')

def github_api(uri, github_token):
    url = f'https://api.github.com{uri}'
    headers={
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + github_token,
        'X-GitHub-Api-Version': '2022-11-28',
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200: # TODO: status_code에 맞춰서 raise Error type 변경
        raise ValueError()
    return res

def create_repo_license_dict(repo_full_name, json):
    return {
        'repo_full_name': repo_full_name,
        'sha': json['sha'],
        'license_key': json['license']['key'],
        'html_url': json['html_url'],
        'download_url': json['download_url'],
        'git_url': json['git_url'],
        'content': json['content'],
        'called_at': datetime.now()
    }

if __name__ == '__main__':
    print("like: nyeong/hanassig")
    repo = input('input repo name: ')
    
    try:
        res = github_api(f'/repos/{repo}/license', github_token)
        repo_license = create_repo_license_dict(repo, res)
    except ValueError:
        print(f'{repo} is not valid')
        exit(1)
    
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_query, repo_license)
                print(f'license info of {repo} added.')
    except Exception as e:
        print(f'something goes wrong with {e}')
