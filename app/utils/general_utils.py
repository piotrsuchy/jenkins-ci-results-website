# general utility functions
import pytz
import socket
import datetime
from flask import current_app

def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        # local_ip = "127.0.0.1"
        print(Exception)
    return local_ip


def get_hostname():
    try:
        hostname = socket.gethostname()
    except Exception:
        print(Exception)
    return hostname


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
