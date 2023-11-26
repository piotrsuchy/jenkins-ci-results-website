# general utility functions
import pytz
import socket
import datetime
import subprocess
import urllib.request
from flask import current_app

def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        # local_ip = "127.0.0.1"
        print(Exception)
    return local_ip

def get_public_ip():
    try:
        output = subprocess.check_output("ip route | grep 'src' | awk '{print $9}'", shell=True)
        return output.strip().decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("An error occured while trying to fetch public IP.")
        return None

def get_hostname():
    try:
        hostname = socket.gethostname()
    except Exception:
        print(Exception)
    return hostname

def find_setup_by_ip(setups):
    ip = get_public_ip()
    print(f"Public ip: {ip}")
    for setup in setups:
        if setup["ip"] == ip:
            return setup
    return None

def find_setup_by_hostname(setups):
    hostname = get_hostname()
    for setup in setups:
        if setup["hostname"] == hostname:
            return setup
    return None

def get_current_warsaw_time():
    local_tz = pytz.timezone('Europe/Warsaw')
    return datetime.datetime.now(tz=local_tz).isoformat()
    # return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

def format_datetime_for_frontend(dt_obj):
    if dt_obj is None:
        current_app.logger.info("Received None instead of a datatime object.")
        return None
    timezone = pytz.timezone('Europe/Warsaw')
    aware_dt_obj = timezone.localize(dt_obj)
    formatted_time = aware_dt_obj.strftime('%Y-%m-%d %H:%M:%S.%f%z')
    return formatted_time
