import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

# Connection parameters - replace with your details
db_name = "ci_monitor_db"
db_user = "admin"
db_pass = "admin"
db_host = "127.0.0.1"
db_port = "5432"

# Test the connection
connection = create_connection(db_name, db_user, db_pass, db_host, db_port)

