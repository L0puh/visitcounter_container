import psycopg2
from psycopg2 import sql, errors
import os
import sys
import psycopg2
from psycopg2 import sql
from datetime import datetime


class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT", "5432")
        self.name = os.getenv("DB_NAME", "visitdb")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")

    def _connect(self):
        try:
            return psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    dbname=self.name,
                    user=self.user,
                    password=self.password)
        except Exception as e:
            print(f"Error in connection: {e}")
            return None

    def setup(self):
        conn = self._connect()
        if not conn:
            return False
            
        try:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS visits (
                    id SERIAL PRIMARY KEY,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error in table creation: {e}")
            if conn: conn.close()
            return False
        
        return True

    def check_connection(self):
        conn = None
        try:
            conn = self._connect()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                return True
            return False
        except Exception as e:
            return False

    def add_visit(self):
        conn = self._connect()
        if not conn:
            return None
            
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO visits DEFAULT VALUES;")
            cur.execute("SELECT COUNT(*) FROM visits;")
            total = cur.fetchone()[0]
            cur.execute("SELECT time FROM visits ORDER BY id DESC LIMIT 1;")
            last_time = cur.fetchone()[0]
            conn.commit()
            return {"total": total, "last_time": last_time}
            
        except Exception as e:
            print(f"Error in adding a new visit: {e}")
            return None
        finally:
            cur.close()
            conn.close()



