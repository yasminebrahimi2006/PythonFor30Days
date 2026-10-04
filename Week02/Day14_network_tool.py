import socket
import subprocess
import platform
import sys
from datetime import datetime


def get_hostname():
    """اسم کامپیوتر"""
    return socket.gethostname()


def get_local_ip():
    """IP داخلی"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Not available"


def get_public_ip():
    """IP عمومی (نیاز به اینترنت)"""
    import urllib.request
    try:
        return urllib.request.urlopen("https://api.ipify.org").read().decode()
    except Exception:
        return "No internet"


def ping_host(host, count=4):
    """پینگ گرفتن از یه هاست"""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, str(count), host]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        return result.stdout if result.returncode == 0 else f"Failed to ping {host}"
    except subprocess.TimeoutExpired:
        return "Timeout"


def check_port(host, port):
    """چک کردن یه پورت"""
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def scan_ports(host, ports):
    """اسکن چند پورت"""
    results = {}
    for port in ports:
        results[port] = check_port(host, port)
    return results


def dns_lookup(host):
    """تبدیل دامنه به IP"""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return "DNS lookup failed"


def main():
    print("=" * 50)
    print("🌐 Network Tool")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Hostname: {get_hostname()}")
    print(f"Local IP: {get_local_ip()}")
    print(f"Public IP: {get_public_ip()}")
    print(f"OS: {platform.system()} {platform.release()}")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Ping a host")
        print("2. DNS lookup")
        print("3. Check a port")
        print("4. Scan common ports")
        print("5. Exit")

        choice = input("\nChoose (1-5): ").strip()

        if choice == "1":
            host = input("Host (e.g., google.com): ").strip()
            print(ping_host(host))

        elif choice == "2":
            host = input("Domain (e.g., google.com): ").strip()
            print(f"IP: {dns_lookup(host)}")

        elif choice == "3":
            host = input("Host: ").strip()
            port = int(input("Port: ").strip())
            status = "OPEN " if check_port(host, port) else "CLOSED "
            print(f"Port {port} on {host}: {status}")

        elif choice == "4":
            host = input("Host: ").strip()
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 8080]
            print(f"Scanning {host}...")
            results = scan_ports(host, common_ports)
            for port, is_open in results.items():
                print(f"  Port {port}: {'OPEN ' if is_open else 'closed'}")

        elif choice == "5":
            print("Bye! ")
            sys.exit(0)

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()