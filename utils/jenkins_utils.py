import re
import requests
from utils.db_utils import get_db_connection, release_db_connection

def extract_test_results(description):
    """
    Extracts test results from the description field using a regular expression.
    """
    pattern = r"All Tests: (\d+) tests \((\d+) OK, (\d+) FAIL\)"
    if description and isinstance(description, str):
        match = re.search(pattern, description)
        if match:
            return match.groups()
    return None

def get_latest_builds(job_name):
    results = []
    try:
        response = requests.get("http://janusz.emea.nsn-net.net:8080/job/" + job_name + "api/json?tree=builds[number,url,result,timestamp,duration,description]{0,10}", verify=False)
        response.raise_for_status()
        
        data = response.json()
        builds = data.get("builds", [])
        
        for build in builds:
            entry = {
                "number": build["number"],
                "url": build["url"],
                "status": build.get("result", "IN PROGRESS"),
                "timestamp": build["timestamp"] / 1000,
                "duration": build["duration"] / 1000,
                "description": build.get("description", "")
            }
            test_results = extract_test_results(entry["description"])
            if test_results:
                entry.update({"total_tests": test_results[0], "passed_tests": test_results[1], "failed_tests": test_results[2]})
                results.append(entry)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Jenkins data: {e}")
    return results

def fetch_data_for_setup(setup_id):
    # Fetch setup name for given setup_id from database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM setups WHERE setup_id = %s;", (setup_id,))
    setup_name = cursor.fetchone()[0]
    cursor.close()
    release_db_connection(conn)
    
    # Fetch Jenkins data for the given setup
    # Note: This assumes that setup_name is equivalent to Jenkins job_name
    return get_latest_builds(setup_name)
