# general utility functions

import socket


def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "127.0.0.1"
    return local_ip

def find_setup_by_ip(ip_address, setups):
    for setup in setups:
        if setup["ip"] == ip_address:
            return setup
    return None
