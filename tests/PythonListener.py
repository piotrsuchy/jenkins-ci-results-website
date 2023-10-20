import requests, os
import json, datetime
import pytz
from dotenv import load_dotenv

# Import utilities
from app.utils.general_utils import find_setup_by_hostname
from app.utils.db_utils import (
    get_db_connection,
    release_db_connection,
    get_latest_test_id,
    get_latest_scope_id,
)

load_dotenv()


class PythonListener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, interval=10):
        self.interval = interval

        self.test_start_time = None
        self.scope_start_time = None
        self.running_scope_stack = []
        self.current_scope_name = None
        self.test_name = None
        self.current_scope_id = 0

        self.total_tests_in_scope = None
        self.tests_completed = None

        self.setups = self._read_setups_from_config()
        self.setup_id = self.find_matching_setup()
        # Fetch the latest test_id from the database and use it as the starting point
        conn = self._get_db_connection()
        self.current_test_id = get_latest_test_id(conn)
        self.max_id = get_latest_scope_id(conn)
        release_db_connection(conn)
        
        self.server_address = os.environ.get("CI_MONITOR_SERVER_ADDRESS")

        
    def start_suite(self, data, result):
        self.total_tests_in_scope = len(list(data.tests))
        self.tests_completed = 0
        self.max_id += 1
        self.running_scope_stack.append((self.max_id, data.name))
        self.current_scope_id = self.max_id
        self.current_scope_name = str(data)
        local_tz = pytz.timezone('Europe/Warsaw')
        self.scope_start_time = datetime.datetime.now(tz=local_tz).isoformat()
        self.current_scope_name = str(data)
        suite_data = self._prepare_scope_data_start(result)
        self._post_scope_data(suite_data)
        self.update_progress()

    def start_test(self, data, result):
        # print(f"STARTING TEST WITH ID: {self.current_test_id}")
        conn = self._get_db_connection()
        self.current_test_id = get_latest_test_id(conn) + 1
        release_db_connection(conn)
        local_tz = pytz.timezone('Europe/Warsaw')
        self.test_start_time = datetime.datetime.now(tz=local_tz).isoformat()
        self.test_name = str(data)
        test_data = self._prepare_test_data_start(data)
        self._post_test_data(test_data)
        self.update_progress()

    def end_test(self, data, result):
        self.tests_completed += 1
        test_status = "pass" if result.passed else "fail"
        test_data = self._prepare_test_data_end(test_status)
        self._update_end_time(test_data)

    def end_suite(self, data, result):
        # print(f"---------ENDING SUITE: {self.current_scope_id}")

        scope_status = "pass" if result.passed else "fail"
        
        scope_data = self._prepare_scope_data_end(scope_status)
        self._update_end_time(scope_data)
        self.running_scope_stack.pop()
        if not self.running_scope_stack:
            # print("The whole suite has been ended!")
            self.current_scope_id = None
            self.current_scope_name = None
        else:
            self.current_scope_id = self.running_scope_stack[-1][0]
            self.current_scope_name = self.running_scope_stack[-1][1]
        # print(f"---------ENDING SUITE: {self.current_scope_id}")
        self.tests_completed = 0
        self.total_tests_in_scope = 0
        self.update_progress()

    def _prepare_test_data_start(self, data):
        return {
            "test_name": data.name,
            "start_time": self.test_start_time,
            "scope_id": self.current_scope_id,
            "status": "running",
        }

    def _prepare_test_data_end(self, test_status):
        return {
            "table_name": "tests",
            "id": f"{self.current_test_id}",
            "status": test_status,
        }

    def _prepare_scope_data_start(self, result):
        setup_id = self.find_matching_setup()
        if setup_id is None:
            setup_id = 1

        return {
            "setup_id": setup_id,
            "name": self.current_scope_name,
            "start_time": self.scope_start_time,
            "status": "running",
        }

    def _prepare_scope_data_end(self, scope_status):
        return {
            "table_name": "scopes",
            "id": self.current_scope_id,
            "status": scope_status,
        }

    def _post_test_data(self, test_data):
        requests.post(f"http://{self.server_address}/api/post_test_results", json=test_data)

    def _post_scope_data(self, scope_data):
        response = requests.post(f"http://{self.server_address}/api/post_scope_results", json=scope_data)
        if response.status_code == 200:
            resp_json = response.json()
            if "scope_id" in resp_json:
                self.current_scope_id = resp_json["scope_id"]
        conn = self._get_db_connection()
        release_db_connection(conn)  # Release the connection back to the pool

    def update_progress(self):
        url = f'http://{self.server_address}/api/update_progress/{self.setup_id}'
        data = {
            'completed_tests': self.tests_completed,
            'total_tests': self.total_tests_in_scope
        }
        response = requests.post(url, json=data)
        # print(f"Updating progress to: {self.tests_completed}/{self.total_tests_in_scope}")
        if response.status_code != 200:
            print("Failed to send progress update:", response.content)

    def _update_end_time(self, data):
        requests.put(f"http://{self.server_address}/api/update_end_time", json=data)

    def _read_setups_from_config(self):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        with open(f"{tests_dir}/../setups_config.json", "r") as f:
            return json.load(f)["pipelines"]

    def _get_db_connection(self):
        return get_db_connection()  # Use pooled connection

    def show_progress(self):
        return f"{self.tests_completed}/{self.total_tests_in_scope}"

    def find_matching_setup(self):
        matching_setup = find_setup_by_hostname(self.setups)
        if matching_setup is None:
            print(f"Didn't find any matching setups!!!")
            matching_setup = self.setups[0]
        return matching_setup["setup_id"]

    def get_setup_id(self):
        return self.setup_id
