# Released under the MIT License. See LICENSE for details.
#created by vortex
#edited by sara
from playersData import pdata
from stats import mystats
import setting
import threading

stats = mystats.get_all_stats()
settings = setting.get_settings_data()

top_player_count = settings['autoadmin']['top_rank_count']
admin_rank = settings['autoadmin'].get('admin_rank', [])
admin_score = settings['autoadmin']['score_for_admin']
vip_rank = settings['autoadmin'].get('vip_rank', [])
vip_score = settings['autoadmin']['score_for_vip']
BLUE = '\033[34m'
RESET = '\033[0m'
BLACK = '\033[30m'


def get_top_players(data, count=top_player_count):
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
                print(f"Removed {player_id} from the '{role_name}' role.")
            else:
                print(f"{player_id} not found in '{role_name}' role.")
        
        # Update roles data immediately after removing player IDs
        pdata.updates_roles()
    else:
        print(f"Role '{role_name}' not found in roles.json.")


def add_ids_to_role(role_name, player_ids):
    roles_data = pdata.get_roles()

    if role_name in roles_data:
        role_ids = roles_data[role_name]['ids']
        
        for player_id in player_ids:
            if player_id not in role_ids:
                role_ids.append(player_id)
                print(f"Added player ID {player_id} to the '{role_name}' role.")
            else:
                print(f"Player ID {player_id} is already in the '{role_name}' role.")
        
        # Update roles data immediately after adding player IDs
        pdata.updates_roles()
    else:
        print(f"Role '{role_name}' not found in roles.json.")

        
def get_player_rank_and_score(player_id):
    """Get the rank and score of a player."""
    player_data = stats.get(player_id, {})
    return player_data.get('rank', 0), player_data.get('scores', 0)


# Function to print messages when admin or VIP roles are updated or removed
def print_update_message(role_name, action, player_id):
    print(f"{role_name.capitalize()} {action}: {player_id}")


# Function to remove outdated admins
def remove_outdated_admins():
    if not admin_rank:
        print("No admin ranks specified. Skipping admin role assignment.")
        return
    
    roles_data = pdata.get_roles()
    current_admin_ids = roles_data.get('admin', {}).get('ids', [])
    
    for player_id in current_admin_ids:
        rank, score = get_player_rank_and_score(player_id)
        if rank not in admin_rank and score < admin_score:
            print_update_message('admin', 'removed', player_id)
            remove_all_ids_from_role('admin', [player_id])
    threading.Timer(500, remove_outdated_admins).start()  # Start timer for removing outdated admins

# Function to remove outdated VIPs
def remove_outdated_vips():
    if not vip_rank:
        print("No VIP ranks specified. Skipping VIP role assignment.")
        return
    
    roles_data = pdata.get_roles()
    current_vip_ids = roles_data.get('vip', {}).get('ids', [])
    
    for player_id in current_vip_ids:
        rank, score = get_player_rank_and_score(player_id)
        if rank not in vip_rank and score < vip_score:
            print_update_message('vip', 'removed', player_id)
            remove_all_ids_from_role('vip', [player_id])
    threading.Timer(500, remove_outdated_vips).start()  # Start timer for removing outdated VIPs


# Function to update admins and VIPs
def update_admins_and_vips():
    top_players = get_top_players(stats)
    roles_data = pdata.get_roles()
    current_admin_ids = roles_data.get('admin', {}).get('ids', [])
    current_vip_ids = roles_data.get('vip', {}).get('ids', [])

    for rank, (player_id, player_data) in enumerate(top_players, start=1):
        score = player_data.get('scores', 0)
        if player_id not in roles_data:
            if rank in admin_rank and score >= admin_score and player_id not in current_admin_ids:
                print_update_message('admin', 'added', player_id)
                add_ids_to_role('admin', [player_id])
            elif rank in vip_rank and score >= vip_score and player_id not in current_vip_ids:
                print_update_message('vip', 'added', player_id)
                add_ids_to_role('vip', [player_id])
        else:
            if rank not in admin_rank and score <= admin_score and player_id in current_admin_ids:
                print_update_message('admin', 'removed', player_id)
                remove_all_ids_from_role('admin', [player_id])
            elif rank not in vip_rank and score <= vip_score and player_id in current_vip_ids:
                print_update_message('vip', 'removed', player_id)
                remove_all_ids_from_role('vip', [player_id])
    threading.Timer(500, update_admins_and_vips).start()      


# Start autoadmin functions if enabled
autoadmin_enabled = settings.get('autoadmin', {}).get('enable', False)
if autoadmin_enabled:
    print(f"{BLACK}AutoAdmin is Enabled...{RESET}")
    update_admins_and_vips()
    remove_outdated_admins()
    remove_outdated_vips()
else:
    print(f"{BLACK}AutoAdmin is Disabled. {RESET}")
