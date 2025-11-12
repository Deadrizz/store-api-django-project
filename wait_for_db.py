import time
import psycopg2
from psycopg2 import OperationalError
import os
DB_HOST = os.getenv('POSTGRES_HOST',"db")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        conn.close()
        print('Database is ready')
        break
    except OperationalError:
        print('Waiting for db')
        time.sleep(2)