from tools import mongo
from playersData import pdata 
import _ba, ba, os
import setting
import json
import threading
from multiprocessing.pool import ThreadPool
import random
settings = setting.get_settings_data()
collection = mongo.playerinfo


def read_profiles_from_file():
    try:
        file_path = os.path.join(_ba.env()['python_directory_user'], "playersData", "profiles.json")
        with open(file_path, 'r') as file:
            profiles_data = json.load(file)
        return profiles_data
    except Exception as e:
        print(f"Error reading profiles from file: {e}")
        return None

def update_mongo_with_profiles():
    try:
        # Read profiles from file
        profiles_data = read_profiles_from_file()
        
        if profiles_data:
            # Update MongoDB with profiles data
            mongo.playerinfo.update_one({}, {"$set": profiles_data}, upsert=True)
            print("Profiles updated successfully.")
        else:
            print("No profiles data found or unable to read from file.")
        
    except Exception as e:
        print(f"Error updating MongoDB with profiles: {e}")

    # Set the timer for the next update after 10 seconds
    threading.Timer(1000, update_mongo_with_profiles).start()

# Start the initial update
update_mongo_with_profiles()


def get_owners_ids():
    roles = pdata.get_roles()
    if roles and 'owner' in roles:
        owner_ids = roles['owner']['ids']
        pb_ids = []  # Initialize the list
        if owner_ids:
            for i in range(len(owner_ids)):
                pb_id = owner_ids[i]
                pb_ids.append(pb_id)  # Append each pb_id to the list
        return pb_ids  # Return the list of pb_ids


def update_server_info(m, server_name, dc_servername, dc_serverid, server_ip, server_port):
    # Construct the updated server info dictionary
    updated_server_info = {
        'name': server_name,
        'ip': server_ip,
        'port': server_port,
        'database_name': settings['discordbot']['database_name'],
        'owner_ids': get_owners_ids(),
        'whitelisted_servers': settings["discordbot"]["whitelisted_servers"],
        'whitelisted_user': settings["discordbot"]["allowed_user_ids"],
        'dc_server_name': dc_servername,
        'dc_server_id': dc_serverid
    }

    # Update existing server information or insert new server information
    result = mongo.serverinfo.replace_one(
        {'serverinfo.name': server_name},
        {'serverinfo': updated_server_info},
        upsert=True
    )

    # Check if the document was modified or inserted
    if result.modified_count > 0:
        print("Your server is updated successfully.")
    else:
        print("Server is already up to date.")
