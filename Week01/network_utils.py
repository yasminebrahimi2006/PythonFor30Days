def is_valid_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

def format_ip(ip):
    return f"IP: {ip}"

def get_local_ip():
    import socket
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "127.0.0.1"