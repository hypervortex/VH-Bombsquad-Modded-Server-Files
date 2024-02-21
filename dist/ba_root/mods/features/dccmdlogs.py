import json
from datetime import datetime
import os
import _ba

# Define the directory path using the playerData variable
directory_path = os.path.join(_ba.env()["python_directory_user"], "playersData")

# Create the directory if it doesn't exist
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Define the file path within the directory
file_path = os.path.join(directory_path, "discord_command_logs.json")  # Adjust the file name as needed

def log_command(user_id, user_name, command):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create or load logs data
    logs_data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            logs_data = json.load(f)
    
    # Append new log entry
    logs_data.append({
        "user_id": user_id,
        "user_name": user_name,
        "command": command,
        "timestamp": timestamp
    })
    
    # Write logs data to JSON file
    with open(file_path, "w") as f:
        json.dump(logs_data, f, indent=4)

    print("Command logged successfully.")

