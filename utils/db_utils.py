# utility functions related to databases

import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
    )
    return conn


def get_setup_id_by_name(setup_name, conn):
    cur = conn.cursor()
    cur.execute("SELECT setup_id FROM setups WHERE name = %s;", (setup_name,))
    result = cur.fetchone()
    return result[0] if result else None
