from .Handlers import handlemsg, handlemsg_all, send, clientid_to_myself, sendall, sendchat
from playersData import pdata
# from tools.whitelist import add_to_white_list, add_commit_to_logs
from serverData import serverdata
import ba
import _ba
import time
import setting
import ba.internal
import _thread
import random
from stats import mystats
from bastd.gameutils import SharedObjects
from tools import playlist
from tools import logger
Commands = ['recents', 'info', 'cm', 'createteam', 'unban', 'showid', 'hideid', 'lm', 'gp', 'party', 'quit', 'kickvote', 'maxplayers', 'playlist', 'server', 'ban', 'kick', 'remove', 'end', 'quit', 'mute', 'unmute', 'slowmo', 'nv', 'dv', 'pause',
            'cameramode', 'createrole', 'ct', 'reflections', 'partyname', 'addrole', 'removerole', 'addcommand', 'addcmd', 'removecommand', 'getroles', 'removecmd', 'changetag', 'customtag', 'customeffect', 'removeeffect', 'removetag', 'add', 'spectators', 'lobbytime']
CommandAliases = ['max', 'rm', 'next', 'restart', 'mutechat', 'unmutechat', 'sm',
                  'slow', 'night', 'fr', 'floorReflection', 'frefl', 'day', 'pn', 'pausegame', 'camera_mode', 'rotate_camera', 'effect']


def ExcelCommand(command, arguments, clientid, accountid):
    """
    Checks The Command And Run Function

    Parameters:
        command : str
        arguments : str
        clientid : int
        accountid : int

    Returns:
        None
    """
    if command in ['recents']:
        get_recents(clientid)
    if command in ['info']:
        get_player_info(arguments, clientid)
    if command in ['maxplayers', 'max']:
        changepartysize(arguments)
    if command in ['createteam', 'ct']:
        create_team(arguments)
    elif command == 'playlist':
        changeplaylist(arguments)
    elif command == 'server':
        server(arguments, clientid)
    elif command == 'kick':
        kick(arguments, clientid, accountid)
    elif command == 'ban':
        ban(arguments, clientid, accountid)
    elif command == 'unban':
        unban(arguments, clientid, accountid)
    elif command in ['end', 'next']:
        end(arguments)
    elif command == 'kickvote':
        kikvote(arguments, clientid)
    elif command == 'hideid':
        hide_player_spec()
    elif command == "showid":
        show_player_spec()
    elif command == 'lm':
        last_msgs(clientid)

    elif command == 'gp':
        get_profiles(arguments, clientid)

    elif command == 'cm':
        cm(arguments, clientid)

    elif command == 'party':
        party_toggle(arguments)

    elif command in ['quit', 'restart']:
        quit(arguments)

    elif command in ['mute', 'mutechat']:
        mute(arguments, clientid)

    elif command in ['unmute', 'unmutechat']:
        un_mute(arguments, clientid)

    elif command in ['remove', 'rm']:
        remove(arguments)

    elif command in ['sm', 'slow', 'slowmo']:
        slow_motion()

    elif command in ['fr', 'floorReflection', 'frefl']:
        reflection(arguments)

    elif command in ['nv', 'night']:
        nv(arguments)

    elif command in ['dv', 'day']:
        dv(arguments)

    elif command in ['pause', 'pausegame']:
        pause()

    elif command in ['cameraMode', 'camera_mode', 'rotate_camera']:
        rotate_camera()

    elif command == 'createrole':
        create_role(arguments)

    elif command == 'addrole':
        add_role_to_player(arguments)

    elif command == 'removerole':
        remove_role_from_player(arguments)

    elif command == 'getroles':
        get_roles_of_player(arguments, clientid)

    elif command == 'reflections':
        reflections(arguments, clientid)

    elif command in ['pn', 'partyname']:
        partyname(arguments, clientid, accountid)

    elif command in ['addcommand', 'addcmd']:
        add_command_to_role(arguments)

    elif command in ['removecommand', 'removecmd']:
        remove_command_to_role(arguments)

    elif command == 'changetag':
        change_role_tag(arguments)

    elif command == 'customtag':
        set_custom_tag(arguments)

    elif command in ['customeffect', 'effect']:
        set_custom_effect(arguments)

    elif command in ['removetag']:
        remove_custom_tag(arguments)

    elif command in ['removeeffect']:
        remove_custom_effect(arguments)

    # elif command in ['add', 'whitelist']:
    #     whitelst_it(accountid, arguments)

    elif command == 'spectators':
        spectators(arguments)

    elif command == 'lobbytime':
        change_lobby_check_time(arguments)


def create_team(arguments):
    if len(arguments) == 0:
        ba.internal.chatmessage("enter team name")
    else:
        from ba._team import SessionTeam
        _ba.get_foreground_host_session().sessionteams.append(SessionTeam(team_id=len(_ba.get_foreground_host_session().sessionteams) + 1, name=str(arguments[0]), color=(random.uniform(0, 1.2), random.uniform(
            0, 1.2), random.uniform(0, 1.2))))
        from ba._lobby import Lobby
        _ba.get_foreground_host_session().lobby = Lobby()


def hide_player_spec():
    _ba.hide_player_device_id(True)


def show_player_spec():
    _ba.hide_player_device_id(False)


def get_player_info(arguments, client_id):
    if len(arguments) == 0:
        send("invalid client id", client_id)
    for account in serverdata.recents:
        if account['client_id'] == int(arguments[0]):
            send(pdata.get_detailed_info(account["pbid"]), client_id)


def get_recents(client_id):
    for players in serverdata.recents:
        send(
            f"{players['client_id']} {players['deviceId']} {players['pbid']}", client_id)


def changepartysize(arguments):
    if len(arguments) == 0:
        ba.internal.chatmessage("enter number")
    else:
        ba.internal.set_public_party_max_size(int(arguments[0]))
        ba.internal.chatmessage("Maximum players set to " + str(int(arguments[0])))


def changeplaylist(arguments):
    if len(arguments) == 0:
        ba.internal.chatmessage("enter list code or name")
    else:
        if arguments[0] == 'coop':
            serverdata.coopmode = True
        else:
            serverdata.coopmode = False
        playlist.setPlaylist(arguments[0])
    return


def server(arguments, client_id):
    if arguments == []:
         ba.internal.chatmessage("Usage: /server [name] <text to send>", clients=[client_id])
    else:
        message = ""
        for i in range(1, len(arguments)):
            message += arguments[i] + ''
    ba.internal.chatmessage(message, sender_override=arguments[0])


def partyname(arguments, client_id, ac_id):
    if arguments == []:
         ba.internal.chatmessage("Usage: /partyname Name of party", clients=[client_id])
    else:
        stats = mystats.get_stats_by_id(ac_id)
        myself = stats["name"]
        name = " "
        for word in arguments:
            name+= word+" "
        try:
            ba.internal.set_public_party_name(name)
            _ba.screenmessage(f"{myself} Changed PartyName To {name}", color=(1,1,1), transient=True)
        except:
            _ba.screenmessage("failed to change PartyName", color=(1,1,1), transient=True, clients=[client_id])


def kick(arguments, clientid, ac_id):
    cl_id = int(arguments[0])
    for me in ba.internal.get_game_roster():
        if me["client_id"] == clientid:
            myself = me["display_string"]
    for ros in ba.internal.get_game_roster():
        if ros["client_id"] == cl_id:
            logger.log(f'kicked {ros["display_string"]}')
            sendchat(f'{myself} kicked {ros["display_string"]} Goodbye 👋')
    ba.internal.disconnect_client(int(arguments[0]))
    return

def kikvote(arguments, clientid):
    if arguments == [] or arguments == [''] or len(arguments) < 2:
        return

    elif arguments[0] == 'enable':
        if arguments[1] == 'all':
            _ba.set_enable_default_kick_voting(True)
        else:
            try:
                cl_id = int(arguments[1])
                for ros in ba.internal.get_game_roster():
                    if ros["client_id"] == cl_id:
                        pdata.enable_kick_vote(ros["account_id"])
                        logger.log(
                            f'kick vote enabled for {ros["account_id"]} {ros["display_string"]}')
                        send(
                            "Upon server restart, Kick-vote will be enabled for this person", clientid)
                return
            except:
                return

    elif arguments[0] == 'disable':
        if arguments[1] == 'all':
            _ba.set_enable_default_kick_voting(False)
        else:
            try:
                cl_id = int(arguments[1])
                for ros in ba.internal.get_game_roster():
                    if ros["client_id"] == cl_id:
                        _ba.disable_kickvote(ros["account_id"])
                        send("Kick-vote disabled for this person", clientid)
                        logger.log(
                            f'kick vote disabled for {ros["account_id"]} {ros["display_string"]}')
                        pdata.disable_kick_vote(
                            ros["account_id"], 2, "by chat command")
                return
            except:
                return
    else:
        return


def last_msgs(clientid):
    for i in ba.internal.get_chat_messages():
        send(i, clientid)


def get_profiles(arguments, clientid):
    try:
        playerID = int(arguments[0])
        num = 1
        for i in ba.internal.get_foreground_host_session().sessionplayers[playerID].inputdevice.get_player_profiles():
            try:
                send(f"{num})-  {i}", clientid)
                num += 1
            except:
                pass
    except:
        pass


def party_toggle(arguments):
    if arguments == ['public']:
        ba.internal.set_public_party_enabled(True)
        ba.internal.chatmessage("party is public now")
    elif arguments == ['private']:
        ba.internal.set_public_party_enabled(False)
        ba.internal.chatmessage("party is private now")
    else:
        pass


def end(arguments):
    if arguments == [] or arguments == ['']:
        try:
            with _ba.Context(_ba.get_foreground_host_activity()):
                _ba.get_foreground_host_activity().end_game()
        except:
            pass


def ban(arguments, clientid, ac_id):
    try:
        cl_id = int(arguments[0])
        duration = int(arguments[1]) if len(arguments) >= 2 else 0.5
        for me in ba.internal.get_game_roster():
            if me["client_id"] == clientid:
                myself = me["display_string"]
        for ros in ba.internal.get_game_roster():
            if ros["client_id"] == cl_id:
                pdata.ban_player(ros['account_id'], duration,
                                 "by chat command")
                logger.log(f'banned {ros["display_string"]} by chat command')
                sendchat(f'{myself} banned {ros["display_string"]} Goodbye 👋')
        ba.internal.disconnect_client(int(arguments[0]))
        ## backup part 
        for account in serverdata.recents:  # backup case if player left the server
            if account['client_id'] == int(arguments[0]):
                pdata.ban_player(
                    account["pbid"], duration, "by chat command")
                logger.log(
                    f'banned {account["deviceId"]} by chat command, recents')
        ba.internal.disconnect_client(account['client_id'])         
    except:
        pass


def unban(arguments, clientid, ac_id):
    try:
        cl_id = int(arguments[0])
        for me in ba.internal.get_game_roster():
            if me["client_id"] == clientid:
                myself = me["display_string"]
        for account in serverdata.recents:  # backup unban if u by mistakely ban anyone
            if account['client_id'] == cl_id:
                pdata.unban_player(account["pbid"])
                logger.log(
                    f'unbanned {account["deviceId"]} by chat command')
                sendchat(f'{myself} unbanned {account["deviceId"]} from recents') 
    except:
        pass


def quit(arguments):
    if arguments == [] or arguments == ['']:
        logger.log(
            f'Server Restarting, Please Join in a moment !')
        sendall("Server Restarting, Please Join in a moment !")
        ba.quit()

           
def mute(arguments, clientid):
    if len(arguments) == 0:
        serverdata.muted = True
    try:
        cl_id = int(arguments[0])
        duration = int(arguments[1]) if len(arguments) >= 2 else 0.5
        for me in ba.internal.get_game_roster():
            if me["client_id"] == clientid:
                myself = me["display_string"]
        for ros in ba.internal.get_game_roster():
            if ros["client_id"] == cl_id:
                ac_id = ros['account_id']
                logger.log(f'muted {ros["display_string"]}')                
                pdata.mute(ac_id, duration, "muted by chat command")
                sendchat(f'{myself} muted {ros["display_string"]}') 
                return
        for account in serverdata.recents:  # backup case if player left the server
            if account['client_id'] == int(arguments[0]):
                pdata.mute(account["pbid"],  duration,
                           "muted by chat command, from recents")
    except:
        pass
    return


def un_mute(arguments, clientid):
    if len(arguments) == []:
        serverdata.muted = False
    try:
        cl_id = int(arguments[0])
        for me in ba.internal.get_game_roster():
            if me["client_id"] == clientid:
                myself = me["display_string"]        
        for ros in ba.internal.get_game_roster():
            if ros["client_id"] == cl_id:
                pdata.unmute(ros['account_id'])
                logger.log(f'unmuted {ros["display_string"]} by chat command')
                sendchat(f'{myself} unmuted {ros["display_string"]}') 
                return
        for account in serverdata.recents:  # backup case if player left the server
            if account['client_id'] == int(arguments[0]):
                pdata.unmute(account["pbid"])
                logger.log(
                    f'unmuted {ros["display_string"]} by chat command, recents')
    except:
        pass


def remove(arguments):

    if arguments == [] or arguments == ['']:
        return

    elif arguments[0] == 'all':
        session = ba.internal.get_foreground_host_session()
        for i in session.sessionplayers:
            i.remove_from_game()

    else:
        try:
            session = ba.internal.get_foreground_host_session()
            for i in session.sessionplayers:
                if i.inputdevice.client_id == int(arguments[0]):
                    i.remove_from_game()
        except:
            return


def slow_motion():

    activity = _ba.get_foreground_host_activity()

    if activity.globalsnode.slow_motion != True:
        activity.globalsnode.slow_motion = True

    else:
        activity.globalsnode.slow_motion = False


def reflection(arguments):

    activity = _ba.get_foreground_host_activity()

    if activity.globalsnode.floor_reflection != True:
        activity.globalsnode.floor_reflection = arguments[0]

    else:
        activity.globalsnode.floor_reflection = False


def nv(arguments):

    activity = _ba.get_foreground_host_activity()

    if arguments == [] or arguments == ['']:

        if activity.globalsnode.tint != (0.5, 0.7, 1.0):
            activity.globalsnode.tint = (0.5, 0.7, 1.0)
        else:
            # will fix this soon
            pass

    elif arguments[0] == 'off':
        if activity.globalsnode.tint != (0.5, 0.7, 1.0):
            return
        else:
            pass


def dv(arguments):

    activity = _ba.get_foreground_host_activity()

    if arguments == [] or arguments == ['']:

        if activity.globalsnode.tint != (1, 1, 1):
            activity.globalsnode.tint = (1, 1, 1)
        else:
            # will fix this soon
            pass

    elif arguments[0] == 'off':
        if activity.globalsnode.tint != (1, 1, 1):
            return
        else:
            pass


def reflections(arguments, clientid):
    if len(arguments) < 2:
         ba.internal.chatmessage("Usage: /reflections type (1/0) scale", clients=[clientid])
    else:
         rs = [
          int(arguments[1])]
         typee = 'soft' if int(arguments[0]) == 0 else 'powerup'
         try:
             _ba.get_foreground_host_activity().map.node.reflection = typee
             _ba.get_foreground_host_activity().map.node.reflection_scale = rs 
         except:
             pass
         else:
             try:         
                 _ba.get_foreground_host_activity().map.bg.reflection = typee
                 _ba.get_foreground_host_activity().map.bg.reflection_scale = rs
             except:
                 pass
             else:
                 try:
                     _ba.get_foreground_host_activity().map.floor.reflection = typee
                     _ba.get_foreground_host_activity().map.floor.reflection_scale = rs      
                 except:
                     pass        
                 else:
                     try:      
                         _ba.get_foreground_host_activity().map.center.reflection = typee
                         _ba.get_foreground_host_activity().map.center.reflection_scale = rs 
                     except:
                         pass                                 


def cm(arguments, clientid):     
  with _ba.Context(_ba.get_foreground_host_activity()):
    activity = _ba.get_foreground_host_activity()

    if arguments == []:
        time = 2
    else:
        time = int(arguments[0])      
        op = 0.08
        std = activity.globalsnode.vignette_outer
        ba.animate_array(activity.globalsnode, 'vignette_outer', 3, {0:activity.globalsnode.vignette_outer, 10.0:(0,1,0)})
                            
        try:
            _ba.get_foreground_host_activity().map.node.opacity = op
        except:
            pass
        try:
            _ba.get_foreground_host_activity().map.bg.opacity = op
        except:
            pass
        try:
            _ba.get_foreground_host_activity().map.bg.node.opacity = op
        except:
            pass
        try:
            _ba.get_foreground_host_activity().map.node1.opacity = op
        except:
            pass
        try:
            _ba.get_foreground_host_activity().map.node2.opacity = op
        except:
            pass
        try:
            _ba.get_foreground_host_activity().map.node3.opacity = op
        except:
            pass
        try:
            _ba.get_foreground_host_activity().map.steps.opacity = op
        except:
            pass
        try:
            _ba.get_foreground_host_activity().map.floor.opacity = op
        except:
            pass
        try:
            _ba.get_foreground_host_activity().map.center.opacity = op
        except:
            pass
                            
        def off():
            op = 0.57
            try:
                _ba.get_foreground_host_activity().map.node.opacity = op
            except:
                pass
            try:
                _ba.get_foreground_host_activity().map.bg.opacity = op
            except:
                pass
            try:
                _ba.get_foreground_host_activity().map.bg.node.opacity = op
            except:
                pass
            try:
                _ba.get_foreground_host_activity().map.node1.opacity = op
            except:
                pass
            try:
                _ba.get_foreground_host_activity().map.node2.opacity = op
            except:
                pass
            try:
                _ba.get_foreground_host_activity().map.node3.opacity = op
            except:
                pass
            try:
                _ba.get_foreground_host_activity().map.steps.opacity = op
            except:
                pass
            try:
                _ba.get_foreground_host_activity().map.floor.opacity = op
            except:
                pass
            try:
                _ba.get_foreground_host_activity().map.center.opacity = op
            except:
                pass
            ba.animate_array(activity.globalsnode, 'vignette_outer', 3, {0:activity.globalsnode.vignette_outer, 100:std})
        ba.Timer(2.0, ba.Call(off))


def pause():

    activity = _ba.get_foreground_host_activity()

    if activity.globalsnode.paused != True:
        activity.globalsnode.paused = True

    else:
        activity.globalsnode.paused = False


def rotate_camera():

    activity = _ba.get_foreground_host_activity()

    if activity.globalsnode.camera_mode != 'rotate':
        activity.globalsnode.camera_mode = 'rotate'

    else:
        activity.globalsnode.camera_mode = 'follow'


def create_role(arguments):
    try:
        pdata.create_role(arguments[0])
    except:
        return


def add_role_to_player(arguments):
    try:

        session = ba.internal.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[1]):
                roles = pdata.add_player_role(
                    arguments[0], i.get_v1_account_id())
    except:
        return


def remove_role_from_player(arguments):
    try:
        session = ba.internal.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[1]):
                roles = pdata.remove_player_role(
                    arguments[0], i.get_v1_account_id())

    except:
        return


def get_roles_of_player(arguments, clientid):
    try:
        session = ba.internal.get_foreground_host_session()
        roles = []
        reply = ""
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[0]):
                roles = pdata.get_player_roles(i.get_v1_account_id())
                print(roles)
        for role in roles:
            reply = reply+role+","
        send(reply, clientid)
    except:
        return


def change_role_tag(arguments):
    try:
        pdata.change_role_tag(arguments[0], arguments[1])
    except:
        return


def set_custom_tag(arguments):
    try:
        session = ba.internal.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[1]):
                roles = pdata.set_tag(arguments[0], i.get_v1_account_id())
    except:
        return


def remove_custom_tag(arguments):
    try:
        session = ba.internal.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[0]):
                pdata.remove_tag(i.get_v1_account_id())
    except:
        return


def remove_custom_effect(arguments):
    try:
        session = ba.internal.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[0]):
                pdata.remove_effect(i.get_v1_account_id())
    except:
        return


def set_custom_effect(arguments):
    try:
        session = ba.internal.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[1]):
                pdata.set_effect(arguments[0], i.get_v1_account_id())
    except:
        return


all_commands = ["changetag", "createrole", "addrole", "removerole", "addcommand", "addcmd", "removecommand", "removecmd", "kick", "remove", "rm", "end", "next", "quit", "restart", "mute", "mutechat", "unmute", "unmutechat", "sm", "slow", "slowmo", "nv", "night", "dv", "day", "pause", "pausegame", "cameraMode",
                "camera_mode", "rotate_camera", "kill", "die", "heal", "heath", "curse", "cur", "sleep", "sp", "superpunch", "gloves", "punch", "shield", "protect", "freeze", "ice", "unfreeze", "thaw", "gm", "godmode", "fly", "inv", "invisible", "hl", "headless", "creepy", "creep", "celebrate", "celeb", "spaz"]


def add_command_to_role(arguments):
    try:
        if len(arguments) == 2:
            pdata.add_command_role(arguments[0], arguments[1])
        else:
            ba.internal.chatmessage("invalid command arguments")
    except:
        return


def remove_command_to_role(arguments):
    try:
        if len(arguments) == 2:
            pdata.remove_command_role(arguments[0], arguments[1])
    except:
        return


# def whitelst_it(accountid : str, arguments):
#     settings = setting.get_settings_data()

#     if arguments[0] == 'on':
#         if settings["white_list"]["whitelist_on"]:
#             ba.internal.chatmessage("Already on")
#         else:
#             settings["white_list"]["whitelist_on"] = True
#             setting.commit(settings)
#             ba.internal.chatmessage("whitelist on")
#             from tools import whitelist
#             whitelist.Whitelist()
#         return

#     elif arguments[0] == 'off':
#         settings["white_list"]["whitelist_on"] = False
#         setting.commit(settings)
#         ba.internal.chatmessage("whitelist off")
#         return

    # else:
    #     rost = ba.internal.get_game_roster()

    #     for i in rost:
    #         if i['client_id'] == int(arguments[0]):
    #             add_to_white_list(i['account_id'], i['display_string'])
    #             ba.internal.chatmessage(str(i['display_string'])+" whitelisted")
    #             add_commit_to_logs(accountid+" added "+i['account_id'])


def spectators(arguments):

    if arguments[0] in ['on', 'off']:
        settings = setting.get_settings_data()

        if arguments[0] == 'on':
            settings["white_list"]["spectators"] = True
            setting.commit(settings)
            ba.internal.chatmessage("spectators on")

        elif arguments[0] == 'off':
            settings["white_list"]["spectators"] = False
            setting.commit(settings)
            ba.internal.chatmessage("spectators off")


def change_lobby_check_time(arguments):
    try:
        argument = int(arguments[0])
    except:
        ba.internal.chatmessage("must type number to change lobby check time")
        return
    settings = setting.get_settings_data()
    settings["white_list"]["lobbychecktime"] = argument
    setting.commit(settings)
    ba.internal.chatmessage(f"lobby check time is {argument} now")
