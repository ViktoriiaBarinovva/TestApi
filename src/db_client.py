# src/db_client.py
import psycopg2

class DbClient:
    def __init__(self, host, port, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password
        )
        self.conn.autocommit = True

    def execute(self, query, params=None):
        """Выполнить INSERT/UPDATE/DELETE без возврата результата"""
        with self.conn.cursor() as cur:
            cur.execute(query, params or ())

    def fetchone(self, query, params=None):
        """Получить одну строку"""
        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchone()

    def fetchall(self, query, params=None):
        """Получить все строки"""
        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
