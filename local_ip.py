import socket

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