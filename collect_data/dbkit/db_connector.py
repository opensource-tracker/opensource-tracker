from psycopg2.extras import execute_batch
import psycopg2
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

    def select_data(self):
        pass

    def insert_data(self, query, values):
        _cur = self._database()
        try:
            _cur.execute(query, values)
            self.conn.commit()

            print(f">>> Successfully inserted data into table")

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f">>> failed insert data into table: {e}")

        else:
            _cur.close()

    def insert_bulk_data(self, query, values):  # 해당 함수는 좀 더 보완이 필요함
        _cur = self._database()
        try:
            execute_batch(_cur, query, values)
            self.conn.commit()
            _cur.close()
            print(">>> Successfully inserted data into table")

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f">>> failed insert data into table: {e}")

    def update_date(self, data, attribute):
        pass

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print(">>> db disconnected!!")
