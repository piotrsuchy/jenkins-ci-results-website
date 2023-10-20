# general utility functions
import socket

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

