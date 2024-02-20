from tools import mongo
from playersData import pdata 

def update_player_info(user_acid, acid, device_id, ip):
    # Retrieve player information and message
    profiles = pdata.get_profiles()
    age = profiles[acid]["accountAge"]
    other_account = pdata.get_detailed_pinfo(acid)

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

    if acid not in player_info['pinfo']['pbid']:
        # New player; add player details
        player_info['pinfo']['pbid'].append(acid)
        player_info['pinfo']['name'].append(user_acid)
        player_info['pinfo']['deviceid'].append(device_id)
        player_info['pinfo']['ip'].append(ip)
        player_info['pinfo']['linkedaccount'].append(other_account)
        player_info['pinfo']['accountage'].append(age)
        print(f"New player {acid} added")

    # Update MongoDB document
    mongo.playerinfo.delete_many({})
    mongo.playerinfo.insert_one(player_info)
