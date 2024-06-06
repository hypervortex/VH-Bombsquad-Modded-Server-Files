""" Some useful handlers to reduce lot of code """
import _ba, ba
import ba.internal



def send(msg, clientid):
    """Shortcut To Send Private Msg To Client"""
    for m in msg.split("\n"):
        ba.internal.chatmessage(str(m), clients=[clientid])
    _ba.screenmessage(str(msg), transient=True, clients=[clientid])

def sendchatclid(msg, clientid):
    """Shortcut To Send Private Msg To Client"""
    for m in msg.split("\n"):
        ba.internal.chatmessage(str(m), clients=[clientid])

def sendmsgclid(msg, clientid):
    """Shortcut To Send Private Msg To Client"""
    _ba.screenmessage(str(msg), transient=True, clients=[clientid])

def sendall(msg):
    """Shortcut To Send Private Msg To Client"""
    for m in msg.split("\n"):
        ba.internal.chatmessage(str(m))
    _ba.screenmessage(str(msg), transient=True)

def sendchat(msg):
    """Shortcut To Send Private Msg To Client"""
    for m in msg.split("\n"):
        ba.internal.chatmessage(str(m))

def clientid_to_myself(clientid):
    """Return Player Index Of Self Player"""

    for i , player in  enumerate(_ba.get_foreground_host_activity().players):
        if player.sessionplayer.inputdevice.client_id == clientid:
            return i

def clientid_to_name(clientid):
     """Return Player Display Name"""
     for ros in ba.internal.get_game_roster():
            if ros["client_id"] == clientid:
                myself = ros["display_string"]
                return myself

def handlemsg(client, msg):
    """Handles Spaz Msg For Single Player"""
    activity = _ba.get_foreground_host_activity()
    activity.players[client].actor.node.handlemessage(msg)

def handlemsg_all(msg):
    """Handle Spaz message for all players in activity"""

    activity = _ba.get_foreground_host_activity()

    for i in activity.players:
        i.actor.node.handlemessage(msg)



