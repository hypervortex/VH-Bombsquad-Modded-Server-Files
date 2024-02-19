#thanks to chatgpt 
#edited by SARA
import ba, _ba
#To measure the ping of a server IP using Python with end time - start time code, you can use the `socket` library. Here's an example of how you can do this:

#```python
import socket
import time

def get_game_server_ping(ip_address):
    start_time = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Set a timeout for the connection
    try:
        sock.connect((ip_address, 80))
        end_time = time.time()
        ping_time = (end_time - start_time) * 1000  # Convert to milliseconds
        return ping_time
    except socket.error:
        return None
    finally:
        sock.close()

# Replace '192.0.2.1' with the IP address of the server you want to ping
ip_address = '3.108.196.90'

ping = get_game_server_ping(ip_address)
if ping is not None:
    print(f'Ping to {ip_address} is {ping} ms')
else:
    print(f'Failed to ping {ip_address}')
#```

#In this code, we define a function `get_server_ip_ping` that measures the time it takes to establish a connection to the server IP address. The difference between the end time and start time gives us the ping time in milliseconds.

#Let me know if you need further assistance!
