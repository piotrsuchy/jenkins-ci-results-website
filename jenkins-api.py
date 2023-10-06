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
        print(f"URL: http://janusz.emea.nsn-net.net:8080/job/" + job_name + "api/json?tree=builds[number,url,result,timestamp,duration,description]{0,10}")
        response = requests.get("http://janusz.emea.nsn-net.net:8080/job/" + job_name + "api/json?tree=builds[number,url,result,timestamp,duration,description]{0,10}", verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        builds_info = []
        
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
                build_info = {
                    "setup_name": setup_name,
                    "build_number": number,
                    "status": status,
                    "url": url,
                    "started_at": convert_timestamp_to_local_time(timestamp),
                    "duration": format_duration(duration),
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests
                }
                builds_info.append(build_info)
            else:
                build_info = {
                    "setup_name": setup_name,
                    "build_number": number,
                    "status": status,
                    "url": url,
                    "started_at": convert_timestamp_to_local_time(timestamp),
                    "duration": format_duration(duration)
                }
                builds_info.append(build_info)
        return builds_info
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
    all_setups_data = {}
    
    for pipeline in pipelines:
        pipeline_job_name = pipeline["job_name"]
        pipeline_setup_name = pipeline["setup"]
        builds_info = get_latest_builds(pipeline_job_name, pipeline_setup_name)
        all_setups_data[pipeline_setup_name] = builds_info

    print(json.dumps(all_setups_data, indent=4))

if __name__ == "__main__":
    main()