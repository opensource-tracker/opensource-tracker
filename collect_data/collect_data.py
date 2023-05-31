import datetime
import os
from api_calls.api_orgs import collect_api_orgs
from dbkit.db_connector import psqlConnector
from dbkit.queries import API_ORGS_TABLE_INSERT_SQL


HEADERS = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {os.environ.get("API_TOKEN")}',
    'X-GitHub-Api-Version': '2022-11-28'
}


ORGS = ['moloco', 'woowabros', 'daangn', 'toss',
        'ncsoft', 'line', 'kakao', 'naver', 'nhn']



def run():
    db = psqlConnector()
    CURRENT_TIME = datetime.datetime.now()

    orgs_data = collect_api_orgs(HEADERS, ORGS, CURRENT_TIME)
    for values in orgs_data:
        db.insert_data(API_ORGS_TABLE_INSERT_SQL, values)
    db.disconnect()




if __name__ == "__main__":
    run()
