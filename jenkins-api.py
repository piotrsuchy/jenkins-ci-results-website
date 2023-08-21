import urllib3
import re
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Updated Jenkins URL for the specified job 
JENKINS_URL = "https://janusz.emea.nsn-net.net:8443/job/CI_5G_robot_AVQL_Smoke_Tests_rexIO/api/json?tree=builds[number,url,result,timestamp,duration,description]{0,10}"

def extract_test_results(description):
    """
    Extracts test results from the description field using a regular expression.
    """
    pattern = r"All Tests: (\d+) tests \((\d+) OK, (\d+) FAIL\)"
    match = re.search(pattern, description)
    if match:
        total_tests, passed_tests, failed_tests = match.groups()
        return int(total_tests), int(passed_tests), int(failed_tests)
    return None

def get_latest_builds():
    """
    Fetches information about the latest builds for the specified Jenkins job.
    """
    response = requests.get(JENKINS_URL, verify=False)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    data = response.json()
    builds = data.get("builds", [])
    
    for build in builds:
        number = build["number"]
        url = build["url"]
        status = build.get("result", "IN PROGRESS")
        timestamp = build["timestamp"] / 1000  # Convert to seconds
        duration = build["duration"] / 1000  # Convert to seconds
        description = build.get("description", "")
        
        # Extract test results from description
        test_results = extract_test_results(description)
        if test_results:
            total_tests, passed_tests, failed_tests = test_results
            print(f"Build #{number} - Status: {status}")
            print(f"URL: {url}")
            print(f"Started at: {timestamp} (seconds since epoch)")
            print(f"Duration: {duration} seconds")
            print(f"Total Tests: {total_tests}, Passed Tests: {passed_tests}, Failed Tests: {failed_tests}")
            print("-" * 50)
        else:
            print(f"Build #{number} - Status: {status} (Test results not found in description)")
            print("-" * 50)

# Fetch latest builds
get_latest_builds()
