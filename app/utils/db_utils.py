# db_utils.py

# utility functions related to databases
import os
from dotenv import load_dotenv
from psycopg2.pool import SimpleConnectionPool

load_dotenv()

# Setting up the Connection Pool
DATABASE_POOL = SimpleConnectionPool(
    minconn=1,
    maxconn=5,
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT"),
)


def get_db_connection():
    return DATABASE_POOL.getconn()


def release_db_connection(conn):
    DATABASE_POOL.putconn(conn)


def get_setup_id_by_name(setup_name, conn):
    cur = conn.cursor()
    cur.execute("SELECT setup_id FROM setups WHERE name = %s;", (setup_name,))
    result = cur.fetchone()
    return result[0] if result else None


def tuple_to_dict(t, cursor):
    """Convert a tuple to a dictionary based on cursor description."""
    desc = cursor.description
    return {desc[col][0]: t[col] for col in range(len(t))}

def get_latest_test_id(conn):
    """
    Fetch the latest test_id from the database.
    """
    cur = conn.cursor()
    try:
        query = "SELECT MAX(test_id) FROM tests;"
        cur.execute(query)
        result = cur.fetchone()
        if result and result[0]:
            return result[0]
        return 0
    except Exception as e:
        print(f"Error fetching latest test_id: {e}")
        return 0
    finally:
        cur.close()

def get_latest_scope_id(conn):
    """
    Fetch the latest scope_id from the database.
    """
    cur = conn.cursor()
    try:
        query = "SELECT MAX(scope_id) FROM scopes";
        cur.execute(query)
        result = cur.fetchone()
        if result and result[0]:
            return result[0]
        return 0
    except Exception as e:
        print(f"Error fetching latest running scope_id: {e}")
        return 0
    finally:
        cur.close()