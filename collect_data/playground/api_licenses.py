"""
adhoc.api_licenses에 API 정보를 적재하는 예시 코드 조각입니다
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

github_token = os.getenv('GITHUB_TOKEN')

def github_api(uri, github_token):
    url = f'https://api.github.com{uri}'
    headers={
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + github_token,
        'X-GitHub-Api-Version': '2022-11-28',
    }
    res = requests.get(url, headers=headers)
    return res.json()

def execute_insert_license(cursor, license_dict):
    insert_query = """
    INSERT INTO adhoc.api_licenses
    (key, name, spdx_id, node_id, url, body, permissions, conditions, limitations, called_at)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, [
        license_dict['key'],
        license_dict['name'],
        license_dict['spdx_id'],
        license_dict['node_id'],
        license_dict['url'],
        license_dict['body'],
        license_dict['permissions'],
        license_dict['conditions'],
        license_dict['limitations'],
        datetime.now()
    ])

if __name__ == '__main__':
    res = github_api('/licenses', github_token)

    with conn:
        with conn.cursor() as cursor:
            for license in res:
                key = license["key"]
                print(f'for {key}...')
                license_dict = github_api(f'/licenses/{key}', github_token)
                execute_insert_license(cursor, license_dict)
