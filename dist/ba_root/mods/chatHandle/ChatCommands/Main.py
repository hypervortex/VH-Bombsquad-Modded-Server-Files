# Released under the MIT License. See LICENSE for details.


from .commands import NormalCommands
from .commands import Management
from .commands import Fun
from .commands import Cheats
from .commands import NewCmds
from .commands import CoinCmds

from .Handlers import clientid_to_accountid
from .Handlers import check_permissions
from chatHandle.chatFilter import ChatFilter
from bastd.actor import popuptext
import ba
import _ba
import ba.internal
import setting
from datetime import datetime
from playersData import pdata
from serverData import serverdata

settings = setting.get_settings_data()

def return_role(accountid):
    roles = pdata.get_roles()
    for role in roles:
        if accountid in roles[role]["ids"]:
            return role
    return False


def command_type(command):
    """
    Checks The Command Type

    Parameters:
        command : str

    Returns:
        any
    """
    if command in NormalCommands.Commands or command in NormalCommands.CommandAliases:
        return "Normal"

    if command in Management.Commands or command in Management.CommandAliases:
        return "Manage"

    if command in Fun.Commands or command in Fun.CommandAliases:
        return "Fun"

    if command in Cheats.Commands or command in Cheats.CommandAliases:
        return "Cheats"

    if command in NewCmds.Commands or command in NewCmds.CommandAliases:
        return "NewCmd"

    if command in CoinCmds.Commands or command in CoinCmds.CommandAliases:
        return "CoinCmd"


def Command(msg, clientid):
    command = msg.lower().split(" ")[0].split("/")[1]
    arguments = msg.lower().split(" ")[1:]
    accountid = clientid_to_accountid(clientid)
    ARGUMENTS = msg.upper().split(" ")[1:]
    
    role = return_role(accountid)
    if role == 'owner':
        reply = '\ue049|| \ue00cCOMMAND ACCEPTED OWNER\ue00c ||\ue049'
    elif role in ['co-owner', 'coowner']:
        reply = '\ue049|| \ue00cCOMMAND ACCEPTED CO-OWNER\ue00c ||\ue049'
    elif role == 'admin':
        reply = '\ue049|| \ue00cCOMMAND ACCEPTED ADMIN\ue00c ||\ue049'
    elif role == 'vip':
        reply = '\ue049|| \ue00cCOMMAND ACCEPTED VIP\ue00c ||\ue049'
    elif role == 'moderator':
        reply = '\ue049|| \ue00cCOMMAND ACCEPTED MODERATOR\ue00c ||\ue049'
    elif role in ['leadstaff', 'lead-staff']:
        reply = '\ue049|| \ue00cCOMMAND ACCEPTED LEAD-STAFF\ue00c ||\ue049'
    elif role == 'tcs':
        reply = '\ue049|| \ue00cCOMMAND ACCEPTED T-CS\ue00c ||\ue049'
    elif role in ['cs', 'staff']:
        reply = '\ue049|| \ue00cCOMMAND ACCEPTED CS\ue00c ||\ue049'
    
    else:
        reply = '\ue043|| PLAYER COMMAND ACCEPTED ||\ue043'

    if command_type(command) == "Normal":
        NormalCommands.ExcelCommand(command, arguments, clientid, accountid, ARGUMENTS)     

    elif command_type(command) == "CoinCmd":
        CoinCmds.CoinCommands(command, arguments, clientid, accountid)                
            
    elif command_type(command) == "Manage":
        if check_permissions(accountid, command):
            Management.ExcelCommand(command, arguments, clientid, accountid)
            _ba.screenmessage(reply, color=(0,1,0), transient=True)
        else:
            _ba.screenmessage(u"\ue049|| \ue00cCOMMAND NOT FOR KIDS\ue00c ||\ue049", color=(1, 0, 0), transient=True,
                              clients=[clientid])


    elif command_type(command) == "Fun":
        if check_permissions(accountid, command):
            Fun.ExcelCommand(command, arguments, clientid, accountid)
            _ba.screenmessage(reply, color=(0,1,0), transient=True)
        else:
            _ba.screenmessage(u"\ue049|| \ue00cCOMMAND NOT FOR KIDS\ue00c ||\ue049", color=(1, 0, 0), transient=True,
                              clients=[clientid])


    elif command_type(command) == "Cheats":
        if check_permissions(accountid, command):
            Cheats.ExcelCommand(command, arguments, clientid, accountid)
            _ba.screenmessage(reply, color=(0,1,0), transient=True)
        else:
            _ba.screenmessage(u"\ue049|| \ue00cCOMMAND NOT FOR KIDS\ue00c ||\ue049", color=(1, 0, 0), transient=True,
                              clients=[clientid])


    elif command_type(command) == "NewCmd":
        if check_permissions(accountid, command):
            NewCmds.NewCommands(command, arguments, clientid, accountid)     
            _ba.screenmessage(reply, color=(0,1,0), transient=True)
        else:
            _ba.screenmessage(u"\ue049|| \ue00cCOMMAND NOT FOR KIDS\ue00c ||\ue049", color=(1, 0, 0), transient=True,
                              clients=[clientid])                         
    now = datetime.now()
    if accountid in pdata.get_blacklist()["muted-ids"] and now < datetime.strptime(pdata.get_blacklist()["muted-ids"][accountid]["till"], "%Y-%m-%d %H:%M:%S"):

        _ba.screenmessage("You are on mute", transient=True,
                          clients=[clientid])
        return None
    if serverdata.muted:
        return None
    if settings["ChatCommands"]["BrodcastCommand"]:
        return msg
    return None


def QuickAccess(msg, client_id):
    if msg.startswith(","):
        name = ""
        teamid = 0
        for i in ba.internal.get_foreground_host_session().sessionplayers:
            if i.inputdevice.client_id == client_id:
                teamid = i.sessionteam.id
                name = i.getname(True)

        for i in ba.internal.get_foreground_host_session().sessionplayers:
            if hasattr(i, 'sessionteam') and i.sessionteam and teamid == i.sessionteam.id and i.inputdevice.client_id != client_id:
                _ba.screenmessage(name + ":" + msg[1:], clients=[i.inputdevice.client_id],
                                  color=(0.3, 0.6, 0.3), transient=True)

        return None
    elif msg.startswith("."):
        msg = msg[1:]
        msgAr = msg.split(" ")
        if len(msg) > 25 or int(len(msg) / 5) > len(msgAr):
            _ba.screenmessage("msg/word length too long",
                              clients=[client_id], transient=True)
            return None
        msgAr.insert(int(len(msgAr) / 2), "\n")
        for player in _ba.get_foreground_host_activity().players:
            if player.sessionplayer.inputdevice.client_id == client_id and player.actor.exists() and hasattr(player.actor.node, "position"):
                pos = player.actor.node.position
                with _ba.Context(_ba.get_foreground_host_activity()):
                    popuptext.PopupText(
                        " ".join(msgAr), (pos[0], pos[1] + 1, pos[2])).autoretain()
                return None
        return None
