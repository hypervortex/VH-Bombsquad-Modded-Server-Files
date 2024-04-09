# Released under the MIT License. See LICENSE for details.
#created by vortex
#edited by sara
from playersData import pdata
from stats import mystats
import setting
stats = mystats.get_all_stats()
settings = setting.get_settings_data()

top_player_count = settings['autoadmin']['top_rank_count']
admin_rank = settings['autoadmin']['admin_rank']
admin_score = settings['autoadmin']['score_for_admin']
vip_rank = settings['autoadmin']['vip_rank']
vip_score = settings['autoadmin']['score_for_vip']
BLUE = '\033[34m'
RESET = '\033[0m'
BLACK = '\033[30m'
##
## Check if autoadmin is enabled
autoadmin_enabled = settings.get('autoadmin', {}).get('enable', False)
if autoadmin_enabled:
    print(f"{BLACK}AutoAdmin is Enabled...{RESET}")
##
    ## Validate and handle blank or empty admin_rank setting
    admin_ranks = settings['autoadmin'].get('admin_rank', [])
    if not admin_ranks:
        print(f"{BLUE}No admin ranks specified. Skipping admin role assignment.{RESET}")
    else:
        pass
##
    ## Validate and handle blank or empty vip_rank setting
    vip_ranks = settings['autoadmin'].get('vip_rank', [])
    if not vip_ranks:
        print(f"{BLUE}No VIP ranks specified. Skipping VIP role assignment.{RESET}")
    else:
        pass
##
##
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
        if rank not in admin_rank and score < admin_score:
            print(f"Removing admin ID: {player_id}")
            remove_all_ids_from_role('admin', [player_id])

def remove_outdated_vips():
    """Remove outdated vips based on specified conditions."""
    roles_data = pdata.get_roles()
    current_vip_ids = roles_data.get('vip', {}).get('ids', [])
    
    for player_id in current_vip_ids:
        rank, score = get_player_rank_and_score(player_id)
        if rank not in vip_rank and score < vip_score:
            print(f"Removing VIP ID: {player_id}")
            remove_all_ids_from_role('vip', [player_id])


def update_admins_and_vips():
    top_player = get_top_players(stats)
    roles_data = pdata.get_roles()
    current_admin_ids = roles_data.get('admin', {}).get('ids', [])
    current_vip_ids = roles_data.get('vip', {}).get('ids', [])

    for rank, (player_id, player_data) in enumerate(top_player, start=1):
        score = player_data.get('scores', 0)
        if player_id not in roles_data:
            if rank in admin_rank and score >= admin_score and player_id not in current_admin_ids:
                add_ids_to_role('admin', [player_id])
            elif rank in vip_rank and score >= vip_score and player_id not in current_vip_ids:
                 add_ids_to_role('vip', [player_id])
        else:
            if rank not in admin_rank and score <= admin_score and player_id in current_admin_ids:
                remove_all_ids_from_role('admin', [player_id])
            elif rank not in vip_rank and score <= vip_score and player_id in current_vip_ids:
                 remove_all_ids_from_role('vip', [player_id])
