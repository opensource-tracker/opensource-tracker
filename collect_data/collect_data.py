import datetime
import os
from api_calls.api_orgs import collect_api_orgs
from dbkit.db_connector import psqlConnector
from dbkit.queries import *


HEADERS = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {os.environ.get("API_TOKEN")}',
    'X-GitHub-Api-Version': '2022-11-28'
}


ORGS = ['moloco', 'woowabros', 'daangn', 'toss',
        'ncsoft', 'line', 'kakao', 'naver', 'nhn']


def get_current_time():
    """
    현재 시간과 날짜를 문자열 형태로 반환하는 함수입니다.

    Returns:
        str -> 2023-05-30 18:42:24
    """
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")


def run():
    db = psqlConnector()
    CURRENT_TIME = get_current_time()

    orgs_data = collect_api_orgs(HEADERS, ORGS, CURRENT_TIME)
    for values in orgs_data:
        db.insert_data(API_ORGS_TABLE_INSERT_SQL, values)
    db.disconnect()


if __name__ == "__main__":
    run()
