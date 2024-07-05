#by SARA
import socket
from ping3 import ping
import requests

def get_local_ip():
    """
    Retrieves the local IP address of the machine.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually connect to a remote host
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        ip = None
    finally:
        s.close()
    return ip

def get_ip_from_api(api_url="https://api.ipify.org?format=json"):
    """
    Retrieves the public IP address from the specified API.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        return data.get('ip')
    except requests.RequestException as e:
        return None

def get_pings(ip):
    """
    Pings the given IP address and returns the latency.
    """
    try:
        latency = ping(ip)
        if latency is None:
            return f"Ping request to {ip} timed out."
        else:
            return f"{latency * 10000:.2f} ms"
    except Exception as e:
        return f"An error occurred: {e}"


def get_ping():
    ip = get_local_ip()
    if not ip:
        ip = get_ip_from_api()

    if ip:
        return get_pings(ip)
    else:
        return "Could not retrieve any IP address."


def get_ip():
    ip = get_local_ip()
    if not ip:
        ip = get_ip_from_api()

    if ip:
        return ip
    else:
        return "Could not retrieve any IP address."

