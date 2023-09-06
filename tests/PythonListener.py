import requests, os
import json
from dotenv import load_dotenv
import psycopg2

# Import utilities
from utils.general_utils import get_local_ip, find_setup_by_ip
from utils.db_utils import get_setup_id_by_name

load_dotenv()


class PythonListener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, interval=10):
        self.interval = interval
        self.completed_tests = 0

    def log_message(self, message):
        # Suppress all log messages
        pass

    def end_test(self, data, result):
        test_data = {
            "test_name": data.name,
            "duration": result.elapsedtime / 1000,  # Convert milliseconds to seconds
        }
        requests.post("http://127.0.0.1:5000/post_test_results", json=test_data)

    def end_suite(self, data, result):
        # Read setups from setups_config.json
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        with open(f"{tests_dir}/../setups_config.json", "r") as f:
            setups = json.load(f)["pipelines"]

        local_ip = get_local_ip()
        matching_setup = find_setup_by_ip(local_ip, setups)

        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
        )

        if matching_setup:
            setup_name = matching_setup["setup"]
            scope_name = matching_setup["job_name"]
            setup_id = get_setup_id_by_name(
                setup_name, conn
            )  # get setup_id from database
        else:
            setup_id = "Unknown"
            setup_name = "Unknown"

        scope_data = {
            "setup_id": setup_id,
            "name": scope_name,
            "duration": result.elapsedtime / 1000,
        }

        requests.post("http://127.0.0.1:5000/post_scope_results", json=scope_data)
