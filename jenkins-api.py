import requests

# Jenkins URL for the specified job's last build
JENKINS_URL = "https://ci.jenkins.io/job/Core/job/jenkins/job/PR-8388/lastBuild/api/json"

def get_latest_builds():
    """
    Fetches information about the latest builds for the specified Jenkins job.
    """
    response = requests.get(JENKINS_URL)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    data = response.json()
    builds = data.get("builds", [])
    
    for build in builds:
        number = build["number"]
        url = build["url"]
        status = build.get("result", "IN PROGRESS")
        timestamp = build["timestamp"] / 1000  # Convert to seconds
        duration = build["duration"] / 1000  # Convert to seconds
        
        print(f"Build #{number} - Status: {status}")
        print(f"URL: {url}")
        print(f"Started at: {timestamp} (seconds since epoch)")
        print(f"Duration: {duration} seconds")
        print("-" * 50)

# Fetch latest builds
get_latest_builds()
