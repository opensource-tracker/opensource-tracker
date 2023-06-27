from psycopg2.extras import execute_values
import psycopg2
from psycopg2 import errors
import os


class psqlConnector:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER_NAME'),
            password=os.environ.get('DB_USER_PASSWORD'),
            port=os.environ.get('DB_PORT')
        )

    def _database(self):
        self.cur = self.conn.cursor()
        return self.cur

    def select_data(self, query):
        _cur = self._database()
        _cur.execute(query)
        return _cur.fetchall()

    def insert_data(self, query, values):
        _cur = self._database()
        try:
            execute_values(_cur, query, values)
            self.conn.commit()

        except errors.UniqueViolation:  # api_repos_commits_sha 중복 값 처리
            self.conn.rollback()

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f">>> failed insert data into table: {e}")

        finally:
            _cur.close()

    def update_date(self, data, attribute):
        pass

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print(">>> db disconnected!!")
