import json
import os
import _ba

# Define the directory path using the new_member_count variable
directory_path = os.path.join(_ba.env()["python_directory_user"], "tools")

# Create the directory if it doesn't exist
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Define the file path within the directory
file_path = os.path.join(directory_path, f"last_messages.txt")  # Adjust the file name and path as needed

def last_message_count(msg):
    # Create or append to the new file with the message
    with open(file_path, "a") as f:
        f.write(f"{msg}\n")

    #print(f"New message '{msg}' added to the file '{file_path}'.")
