import requests, os
import json
from dotenv import load_dotenv

# Import utilities
from utils.general_utils import get_local_ip, find_setup_by_ip
from utils.db_utils import (
    get_setup_id_by_name,
    get_db_connection,
    release_db_connection,
)

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
        test_data = self._prepare_test_data(data, result)
        self._post_test_data(test_data)

    def end_suite(self, data, result):
        setups = self._read_setups_from_config()
        scope_data = self._prepare_scope_data(setups, data, result)
        self._post_scope_data(scope_data)

    def _prepare_test_data(self, data, result):
        return {
            "test_name": data.name,
            "duration": result.elapsedtime / 1000,  # Convert milliseconds to seconds
        }

    def _post_test_data(self, test_data):
        requests.post("http://127.0.0.1:5000/post_test_results", json=test_data)

    def _read_setups_from_config(self):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        with open(f"{tests_dir}/../setups_config.json", "r") as f:
            return json.load(f)["pipelines"]

    def _prepare_scope_data(self, setups, data, result):
        local_ip = get_local_ip()
        matching_setup = find_setup_by_ip(local_ip, setups)

        conn = self._get_db_connection()

        if matching_setup:
            setup_name = matching_setup["setup"]
            scope_name = matching_setup["job_name"]
            setup_id = get_setup_id_by_name(
                setup_name, conn
            )  # get setup_id from database
        else:
            setup_id = "Unknown"
            scope_name = "Unknown"

        return {
            "setup_id": setup_id,
            "name": scope_name,
            "duration": result.elapsedtime / 1000,
        }

    def _get_db_connection(self):
        return get_db_connection()  # Use pooled connection

    def _post_scope_data(self, scope_data):
        requests.post("http://127.0.0.1:5000/post_scope_results", json=scope_data)
        conn = self._get_db_connection()
        release_db_connection(conn)  # Release the connection back to the pool
