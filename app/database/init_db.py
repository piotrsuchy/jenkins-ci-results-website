import psycopg2, json
from psycopg2 import sql
from ..utils.db_utils import get_db_connection, release_db_connection

def initialize_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SET timezone='UTC';")
    cur.execute(
        "TRUNCATE setups, scopes, tests, jenkinsinfo, failingtestcases RESTART IDENTITY;"
    )
    conn.commit()
    cur.close()
    release_db_connection(conn)

    populate_setups_table()

# filling setups table with records from config json
def populate_setups_table():
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if table is empty
    cur.execute("SELECT COUNT(*) FROM setups;")
    count = cur.fetchone()[0]
    if count > 0:
        print("Setups table already populated, skipping initialization.")
        cur.close()
        release_db_connection(conn)
        return

    with open("setups_config.json") as f:
        config = json.load(f)

    for pipeline in config["pipelines"]:
        insert_query = psycopg2.sql.SQL(
            "INSERT INTO setups (name, comment) VALUES (%s, %s);"
        )
        cur.execute(insert_query, (pipeline["setup"], pipeline.get("comment", "")))

    conn.commit()
    cur.close()
    release_db_connection(conn)
