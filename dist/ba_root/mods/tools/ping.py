import socket
import subprocess

def get_ping_time(server_address):
    try:
        # Execute the ping command
        result = subprocess.run(['ping', '-c', '1', server_address], capture_output=True, text=True, timeout=5)
        
        # Extract ping time from the output
        if "time=" in result.stdout:
            ping_time = float(result.stdout.split("time=")[1].split(" ")[0]) * 1000  # Convert to milliseconds
            return int(ping_time)  # Convert to integer
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Specify the IP address or hostname of the server you want to ping
server_address = 'example.com'
    # Get the ping time
ping_time = get_ping_time(server_address)

    # Print the ping time if available
if ping_time is not None:
    print(f"Ping time to {server_address}: {ping_time} ms")
else:
    print(f"Failed to ping {server_address}")


def get_hostname(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except socket.herror:
        return "Hostname not found"

# Example usage
ip_address = "8.8.8.8"  # Replace with the IP address you want to look up
hostname = get_hostname(ip_address)
print(f"The hostname for {ip_address} is: {hostname}")
