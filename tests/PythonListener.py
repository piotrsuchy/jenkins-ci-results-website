import requests, os
import json, socket
import psycopg2  
from dotenv import load_dotenv


def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = '127.0.0.1'
    return local_ip

def find_setup_by_ip(ip_address, setups):
    for setup in setups:
        if setup['ip'] == ip_address:
            return setup
    return None

def get_setup_id_by_name(setup_name, conn):
    cur = conn.cursor()
    cur.execute("SELECT setup_id FROM setups WHERE name = %s;", (setup_name,))
    result = cur.fetchone()
    return result[0] if result else None



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
            'test_name': data.name,
            'duration': result.elapsedtime / 1000,  # Convert milliseconds to seconds
        }
        requests.post("http://127.0.0.1:5000/post_test_results", json=test_data)

    def end_suite(self, data, result):
        # Read setups from setups_config.json
        with open('setups_config.json', 'r') as f:
            setups = json.load(f)['pipelines']

        local_ip = get_local_ip()

        matching_setup = find_setup_by_ip(local_ip, setups)

        load_dotenv()
        conn = psycopg2.connect(dbname=os.environ.get("DB_NAME"), 
                                user=os.environ.get("DB_USER"), 
                                password=os.environ.get("DB_PASS"), 
                                host=os.environ.get("DB_HOST"), 
                                port=os.environ.get("DB_PORT"))

        if matching_setup:
            setup_name = matching_setup['setup']
            setup_id = get_setup_id_by_name(setup_name, conn)  # get setup_id from database
        else:
            setup_id = "Unknown"
            setup_name = "Unknown"

        scope_data = {
            'setup_id': setup_id,
            'name': setup_name,
            'duration': result.elapsedtime / 1000,
        }

        requests.post("http://127.0.0.1:5000/post_scope_results", json=scope_data)
