import urllib3
import re
import requests
import json
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_pipelines():
    with open('setups_config.json', 'r') as file:
        data = json.load(file)
        return data['pipelines']


def extract_test_results(description):
    """
    Extracts test results from the description field using a regular expression.
    """
    pattern = r"All Tests: (\d+) tests \((\d+) OK, (\d+) FAIL\)"
    if description and isinstance(description, str): # Check that description is not None and is a string
        match = re.search(pattern, description)
        if match:
            total_tests, passed_tests, failed_tests = match.groups()
            return int(total_tests), int(passed_tests), int(failed_tests)
    return None


def get_latest_builds(job_name, setup_name):
    """
    Fetches information about the latest builds for the specified Jenkins job.
    """
    # Updated Jenkins URL for the specified job 
    try:
        response = requests.get("http://janusz.emea.nsn-net.net:8080/job/" + job_name + "api/json?tree=builds[number,url,result,timestamp,duration,description]{0,10}", verify=False)
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
                print("-"*20 + "PIPELINE: ", setup_name + "-"*20)
                print(f"Build #{number} - Status: {status}")
                print(f"URL: {url}")
                print(f"Started at: {convert_timestamp_to_local_time(timestamp)} (seconds since epoch)")
                print(f"Duration: {format_duration(duration)} seconds")
                print(f"Total Tests: {total_tests}, Passed Tests: {passed_tests}, Failed Tests: {failed_tests}")
                print("-" * 50)
            else:
                print(f"Build #{number} - Status: {status} (Test results not found in description)")
                print("-" * 50)
    except requests.exceptions.RequestException as e:
        # Catching any HTTP errors
        print(f"The URL for {setup_name} doesn't exist or there was an error fetching it.")
        print(f"Details: {e}")
        print(f"-------------------------------------------------------------------------")


def convert_timestamp_to_local_time(timestamp):
    # Convert to datetime object
    dt_object = datetime.fromtimestamp(timestamp)
    # Convert to local time
    local_dt = dt_object.astimezone()
    # Format it as you wish
    formatted_time = local_dt.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time

def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

def main():
    pipelines = get_pipelines()
    for pipeline in pipelines:
        pipeline_job_name = pipeline["job_name"]
        pipeline_setup_name = pipeline["setup"]
        get_latest_builds(pipeline_job_name, pipeline_setup_name)

if __name__ == "__main__":
    main()