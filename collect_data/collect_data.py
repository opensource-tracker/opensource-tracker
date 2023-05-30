from api_calls.api_orgs import collect_api_orgs
from dbkit.db_connector import psqlConnector
from dbkit.queries import *


ORGS = ['moloco', 'woowabros', 'daangn', 'toss',
        'ncsoft', 'line', 'kakao', 'naver', 'nhn']


def run():
    db = psqlConnector()
    orgs_data = collect_api_orgs(ORGS)
    for values in orgs_data:
        db.insert_data(API_ORGS_TABLE_INSERT_SQL, values)
    db.disconnect()


if __name__ == "__main__":
    run()
