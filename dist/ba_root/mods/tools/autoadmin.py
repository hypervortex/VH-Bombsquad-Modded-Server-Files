# Released under the MIT License. See LICENSE for details.
#created by vortex
from playersData import pdata
from stats import mystats
import setting
stats = mystats.get_all_stats()
settings = setting.get_settings_data()

admin_score = settings['autoadmin']['score_for_admin']
vip_score = settings['autoadmin']['score_for_vip']


def get_top_players(data, count=5):
    sorted_players = sorted(data.items(), key=lambda x: x[1].get('rank', float('inf')))
    top_players = sorted_players[:count]
    return [(player_id, player_data) for player_id, player_data in top_players]



def remove_all_ids_from_role(role_name, player_ids):
    roles_data = pdata.get_roles()
    
    if role_name in roles_data:
        roles = roles_data[role_name]['ids']

        for player_id in player_ids:
            if player_id in roles:
                roles.remove(player_id)
                pdata.updates_roles()
                print(f"Removed {player_id} from the '{role_name}' role.")
            else:
                print(f"{player_id} not found in '{role_name}' role.")

    else:
        print(f"Role '{role_name}' not found in roles.json.")


def add_ids_to_role(role_name, player_ids):
    roles_data = pdata.get_roles()

    if role_name in roles_data:
        role_ids = roles_data[role_name]['ids']
        
        for player_id in player_ids:
            if player_id not in role_ids:
                role_ids.append(player_id)
                pdata.updates_roles()
                print(f"Added player ID {player_id} to the '{role_name}' role.")
            else:
                print(f"Player ID {player_id} is already in the '{role_name}' role.")       
    else:
        print(f"Role '{role_name}' not found in roles.json.")
        
        
def get_player_rank_and_score(player_id):
    """Get the rank and score of a player."""
    player_data = stats.get(player_id, {})
    return player_data.get('rank', 0), player_data.get('scores', 0)


def remove_outdated_admins():
    """Remove outdated admins based on specified conditions."""
    roles_data = pdata.get_roles()
    current_admin_ids = roles_data.get('admin', {}).get('ids', [])
    
    for player_id in current_admin_ids:
        rank, score = get_player_rank_and_score(player_id)
        if rank != 1 and score < admin_score:
            print(f"Removing admin ID: {player_id}")
            remove_all_ids_from_role('admin', [player_id])

def remove_outdated_vips():
    """Remove outdated vips based on specified conditions."""
    roles_data = pdata.get_roles()
    current_vip_ids = roles_data.get('vip', {}).get('ids', [])
    
    for player_id in current_vip_ids:
        rank, score = get_player_rank_and_score(player_id)
        if rank not in [2, 3] and score < vip_score:
            print(f"Removing VIP ID: {player_id}")
            remove_all_ids_from_role('vip', [player_id])


def update_admins_and_vips():
    top3 = get_top_players(stats)
    roles_data = pdata.get_roles()
    current_admin_ids = roles_data.get('admin', {}).get('ids', [])
    current_vip_ids = roles_data.get('vip', {}).get('ids', [])

    for rank, (player_id, player_data) in enumerate(top3, start=1):
        score = player_data.get('scores', 0)
        if player_id not in roles_data:
            if rank == 1 and score >= admin_score and player_id not in current_admin_ids:
                add_ids_to_role('admin', [player_id])
            elif rank in [2, 4] and score >= vip_score and player_id not in current_vip_ids:
                 add_ids_to_role('vip', [player_id])
        else:
            if rank != 1 and score <= admin_score and player_id in current_admin_ids:
                remove_all_ids_from_role('admin', [player_id])
            elif rank not in [2, 4] and score <= vip_score and player_id in current_vip_ids:
                 remove_all_ids_from_role('vip', [player_id])

