from tools import mongo
from playersData import pdata 
import _ba, ba
import setting
#import asyncio
settings = setting.get_settings_data()

def update_player_info(player_data, pb):
    # Check if player_data is None
    if player_data is None:
        print("Player data is None. Unable to update player info.")
        return  # Exit the function
        
    # Extract necessary information from player_data and pb
    name = player_data.get('display_string', [])[0] if player_data.get('display_string') else None
    device_id = player_data.get('deviceUUID')
    ip = player_data.get('lastIP')
    pbid = pb

    # Ensure all extracted values are not None before proceeding
    if name is None or device_id is None or ip is None or pbid is None:
        print("Some player information is missing. Unable to update player info.")
        return  # Exit the function

    # Retrieve the latest document from MongoDB
    player_info = mongo.playerinfo.find_one() or {
        'pinfo': {
            'pbid': [],
            'name': [],
            'deviceid': [],
            'ip': [],
            'linkedaccount': [],
            'accountage': []
        }
    }

    # Append new player information to the existing document
    player_info['pinfo']['pbid'].append(pbid)
    player_info['pinfo']['name'].append(name)
    player_info['pinfo']['deviceid'].append(device_id)
    player_info['pinfo']['ip'].append(ip)
    player_info['pinfo']['linkedaccount'].append([])
    player_info['pinfo']['accountage'].append([])

    # Insert the updated document into MongoDB
    mongo.playerinfo.delete_many({})
    mongo.playerinfo.insert_one(player_info)

    print("Player data inserted successfully.")



def update_pinfo(pbid, name, device_id, ip):
    player_info = mongo.playerinfo.find_one() or {
        'pinfo': {
            'pbid': [],
            'name': [],
            'deviceid': [],
            'ip': [],
            'linkedaccount': [],
            'accountage': []
        }
    }

    # Append new player information to the existing document
    player_info['pinfo']['pbid'].append(pbid)
    player_info['pinfo']['name'].append(name)
    player_info['pinfo']['deviceid'].append(device_id)
    player_info['pinfo']['ip'].append(ip)

    # Insert the updated document into MongoDB
    mongo.playerinfo.delete_many({})
    mongo.playerinfo.insert_one(player_info)

    print("New Player data successfully.")


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
    # Retrieve the latest document from MongoDB for server info
    server_info = mongo.serverinfo.find_one() or {
        'serverinfo': {
            'name': "",
            'ip': "",
            'port': "",
            'database_name': "",
            'owner_ids': [],
            'whitelisted_servers': [],
            'whitelisted_user': [],
            'dc_server_name': "",
            'dc_server_id': ""  
        }
    }

    # Get server IP and port
    database_name = settings['discordbot']['database_name']
    ownerids = get_owners_ids()
    whitelisted_servers = settings["discordbot"]["whitelisted_servers"]
    whitelisted_user = settings["discordbot"]["allowed_user_ids"]

    # Check if the server port already exists
    if server_info['serverinfo']['port'] and server_info['serverinfo']['port'] != server_port:
        #print("Server port already exists. Updating all server information.")
        # Update server name, IP, port, database name, owner IDs, whitelisted servers, and user DC IDs
        server_info['serverinfo']['name'] = server_name
        server_info['serverinfo']['ip'] = server_ip
        server_info['serverinfo']['port'] = server_port
        server_info['serverinfo']['database_name'] = database_name
        server_info['serverinfo']['owner_ids'] = ownerids
        server_info['serverinfo']['whitelisted_servers'] = whitelisted_servers
        server_info['serverinfo']['whitelisted_user'] = whitelisted_user
        server_info['serverinfo']['dc_server_name'] = dc_servername
        server_info['serverinfo']['dc_server_id'] = dc_serverid
        #print(f"{server_info['serverinfo']['name']}")
        #print(f"{server_info['serverinfo']['ip']}")
        #print(f"{server_info['serverinfo']['port']}")
        #print(f"{server_info['serverinfo']['database_name']}")
        #print(f"{server_info['serverinfo']['owner_ids']}")
        #print(f"{server_info['serverinfo']['whitelisted_servers']}")
        #print(f"{server_info['serverinfo']['whitelisted_user']}")
        #print(f"{server_info['serverinfo']['dc_server_name']}")
        #print(f"{server_info['serverinfo']['dc_server_id']}")        
    #else:
        #print("Updating server information.")

        # Check if server name has changed
        if server_info['serverinfo']['name'] != server_name:
            #print("Server name has changed.")
            server_info['serverinfo']['name'] = server_name

        # Check if server ip has changed
        if server_info['serverinfo']['ip'] != server_ip:
            #print("Server ip has changed.")
            server_info['serverinfo']['ip'] = server_ip

        # Check if server port has changed
        if server_info['serverinfo']['port'] != server_port:
            #print("Server port has changed.")
            server_info['serverinfo']['port'] = server_port

        # Check if database name has changed
        if server_info['serverinfo']['database_name'] != database_name:
            #print("Database name has changed.")
            server_info['serverinfo']['database_name'] = database_name

        # Check if owner IDs have changed
        if server_info['serverinfo']['owner_ids'] != ownerids:
            #print("Owner IDs have changed.")
            server_info['serverinfo']['owner_ids'] = ownerids

        # Check if whitelisted servers have changed        
        if server_info['serverinfo']['whitelisted_servers'] != whitelisted_servers:
            #print("Whitelisted servers have changed.")
            server_info['serverinfo']['whitelisted_servers'] = whitelisted_servers

        # Check if user DC IDs have changed        
        if server_info['serverinfo']['whitelisted_user'] != whitelisted_user:
            #print("User DC IDs have changed.")
            server_info['serverinfo']['whitelisted_user'] = whitelisted_user

        if server_info['serverinfo']['dc_server_name'] != dc_servername:
            #print("DC servers name have changed.")
            server_info['serverinfo']['dc_server_name'] = dc_servername

        if server_info['serverinfo']['dc_server_id'] != dc_serverid:
            #print("DC Server IDs have changed.")
            server_info['serverinfo']['dc_server_id'] = dc_serverid

    # Update MongoDB document
    mongo.serverinfo.delete_many({})
    mongo.serverinfo.insert_one(server_info)
    #print(f"{server_info['serverinfo']['name']}")
    #print(f"{server_info['serverinfo']['ip']}")     
    #print(f"{server_info['serverinfo']['port']}")
    #print(f"{server_info['serverinfo']['database_name']}")
    #print(f"{server_info['serverinfo']['owner_ids']}")
    #print(f"{server_info['serverinfo']['whitelisted_servers']}")
    #print(f"{server_info['serverinfo']['whitelisted_user']}")
    #print(f"{server_info['serverinfo']['dc_server_name']}")
    #print(f"{server_info['serverinfo']['dc_server_id']}")     
    #print("Server information updated successfully")

