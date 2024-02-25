from .Handlers import handlemsg, handlemsg_all, send, clientid_to_myself
from playersData import pdata
# from tools.whitelist import add_to_white_list, add_commit_to_logs
from serverData import serverdata
#from chatHandle.ChatCommands.commands import NormalCommands as nc
import ba
import _ba,os,json
import time
import setting
import ba.internal
import _thread
import random
from stats import mystats
from bastd.gameutils import SharedObjects
from tools import playlist
from tools import logger
Commands = ['hug', 'icy', 'spaz', 'zombieall', 'boxall', 'texall', 'kickall', 'ooh', 'spazall', 'acl', 'vcl']
CommandAliases = ['cc', 'ccall', 'control', 'zombie', 'rainbow', 'ooh', 'playsound', 'tex', 'hugall', 'box', 'ac', 'exchange', 'tint', 'say', 'playsound', 'admincmdlist', 'vipcmdlist']


def NewCommands(command, arguments, clientid, accountid):
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
    if command == 'hug':
        hug(arguments, clientid)
        
    elif command == 'hugall':
      	hugall(arguments, clientid)
    
    elif command in ['control', 'exchange']:
        control(arguments, clientid)

    elif command == 'icy':
        icy(arguments, clientid)
        
    elif command in ['cc', 'spaz']:
        spaz(arguments, clientid)

    elif command in ['ccall', 'spazall']:
        spazall(arguments, clientid)
        
    elif command == 'ac':
        ac(arguments, clientid)
        
    elif command == 'tint':
        tint(arguments, clientid)

    elif command == 'box':
        box(arguments, clientid)

    elif command == 'boxall':
        boxall(arguments, clientid)
        
    elif command == 'kickall':
        kickall(arguments, clientid)

    elif command == 'tex':
        tex(arguments, clientid)

    elif command == 'zombie':
        zombie(arguments, clientid)

    elif command == 'zombieall':
        zombieall(arguments, clientid)
 
    elif command == 'texall':
        texall(arguments, clientid)
        
    elif command == 'say':
        server_chat(arguments, clientid)
        
    elif command in ['acl', 'admincmdlist']:
        acl(arguments, clientid)
        
    elif command == 'ooh':
        play_ooh_sound(arguments)

    elif command == 'playsound':
        play_sound(arguments, clientid)

    elif command in ['vcl', 'vipcmdlist']:
        vcl(arguments, clientid)     

           
def hug(arguments, clientid):
    players = _ba.get_foreground_host_activity().players
    player = _ba.get_foreground_host_activity()
    if arguments == [] or arguments == ['']:
     with ba.Context(player):
        send(f"Using: /hugall [or] /hug [player1Index] [player2Index]", clientid)
    else:
        try:
            players[int(arguments[0])].actor.node.hold_node = players[int(arguments[1])].actor.node
        except:
            pass
            
            
def hugall(arguments, clientid):
    players = _ba.get_foreground_host_activity().players
    player = _ba.get_foreground_host_activity()
    with ba.Context(player):    
     try:
         players[0].actor.node.hold_node = players[1].actor.node
     except:
         pass
     try:
         players[1].actor.node.hold_node = players[0].actor.node
     except:
         pass
     try:
         players[2].actor.node.hold_node = players[3].actor.node
     except:
         pass
     try:
         players[3].actor.node.hold_node = players[2].actor.node
     except:
         pass
     try:
          players[4].actor.node.hold_node = players[5].actor.node
     except:
         pass
     try:
         players[5].actor.node.hold_node = players[4].actor.node
     except:
         pass
     try:
         players[6].actor.node.hold_node = players[7].actor.node
     except:
         pass
     try:
         players[7].actor.node.hold_node = players[6].actor.node
     except:
         pass

#KICK ALL :)))))))))        
def kickall(arguments, clientid):
    try:
        for i in _ba.get_game_roster():
            if i['client_id'] != clientid:
                _ba.disconnect_client(i['client_id'])
    except:
        pass
        
        
def server_chat(arguments, clientid):
    if arguments == []:
        ba.screenmessage('Usage: /say <text to send>', transient=True, clients=[clientid])
    else:
        message = " ".join(arguments)
        _ba.chatmessage(message)
        
  
def box(arguments, clientid):
   players = _ba.get_foreground_host_activity().players
   player = _ba.get_foreground_host_activity()
   with ba.Context(player):
    try:
        try:
            if arguments != []:
                n = int(arguments[0])      
            players[n].actor.node.torso_model = ba.getmodel("tnt");
            players[n].actor.node.color_mask_texture = ba.gettexture("tnt");
            players[n].actor.node.color_texture = ba.gettexture("tnt") 
            players[n].actor.node.highlight = (1,1,1)
            players[n].actor.node.color = (1,1,1);
            players[n].actor.node.head_model = None;
            players[n].actor.node.style = "cyborg";
        except:
            send(f"Using: /boxall [or] /box [PlayerID]", clientid)
    except:
        send(f"Using: /boxall [or] /box [PlayerID]", clientid)

         #BOXALL
def boxall(arguments, clientid):
   players = _ba.get_foreground_host_activity().players
   player = _ba.get_foreground_host_activity()
   with ba.Context(player):    
    try:
        for i in players:
            try:
                i.actor.node.torso_model = ba.getmodel("tnt");
                i.actor.node.color_mask_texture = ba.gettexture("tnt");
                i.actor.node.color_texture = ba.gettexture("tnt")
                i.actor.node.highlight = (1,1,1);
                i.actor.node.color = (1,1,1);
                i.actor.node.head_model = None;
                i.actor.node.style = "cyborg";
            except:
                pass
    except:
        pass


def ac(arguments, clientid):
   players = _ba.get_foreground_host_activity().players
   player = _ba.get_foreground_host_activity()
   a = arguments
   with ba.Context(player):
    try:
        if arguments[0] == 'r':
            m = 1.3 if a[1] is None else float(a[1])
            s = 1000 if a[2] is None else float(a[2])
            ba.animate_array(player.globalsnode, 'ambient_color',3, {0: (1*m,0,0), s: (0,1*m,0),s*2:(0,0,1*m),s*3:(1*m,0,0)},True)
        else:
            try:
                if a[1] is not None:
                    player.globalsnode.ambient_color = (float(a[0]),float(a[1]),float(a[2]))
            except:
                pass
    except:
        send(f"Using: '/ac [Red] [Green] [Blue]' or '/ac r [brightness] [speed]'", clientid)


def tint(arguments, clientid):
   players = _ba.get_foreground_host_activity().players
   player = _ba.get_foreground_host_activity()
   a = arguments
   with ba.Context(player):
    try:
        if arguments[0] == 'r':
            m = 1.3 if a[1] is None else float(a[1])
            s = 1000 if a[2] is None else float(a[2])
            ba.animate_array(player.globalsnode, 'tint',3, {0: (1*m,0,0), s: (0,1*m,0),s*2:(0,0,1*m),s*3:(1*m,0,0)},True)
        else:
            try:
                if a[1] is not None:
                    player.globalsnode.tint = (float(a[0]),float(a[1]),float(a[2]))
            except:
                pass
    except:
        send(f"Using: '/tint [Red] [Green] [Blue]' or '/tint r [brightness] [speed]'", clientid)


def spaz(arguments, clientid):
 players = _ba.get_foreground_host_activity().players
 player = _ba.get_foreground_host_activity()
 a = arguments
 with ba.Context(player):
    try:
        try:
            if arguments != []:
                n = int(a[0])
            players[n].actor.node.color_texture = ba.gettexture(a[1]+"Color")
            players[n].actor.node.color_mask_texture = ba.gettexture(a[1]+"ColorMask")
            players[n].actor.node.head_model = ba.getmodel(a[1]+"Head")
            players[n].actor.node.torso_model = ba.getmodel(a[1]+"Torso")
            players[n].actor.node.pelvis_model = ba.getmodel(a[1]+"Pelvis")
            players[n].actor.node.upper_arm_model = ba.getmodel(a[1]+"UpperArm")
            players[n].actor.node.forearm_model = ba.getmodel(a[1]+"ForeArm")
            players[n].actor.node.hand_model = ba.getmodel(a[1]+"Hand")
            players[n].actor.node.upper_leg_model = ba.getmodel(a[1]+"UpperLeg")
            players[n].actor.node.lower_leg_model = ba.getmodel(a[1]+"LowerLeg")
            players[n].actor.node.toes_model = ba.getmodel(a[1]+"Toes")
            players[n].actor.node.style = (a[1])
        except:
            send(f"Using: /spazall [AppearanceName] [or] /spaz [PlayerID] [AppearanceName] \n________________|_AppearanceName_|_______________\n {'ali, wizard, cyborg, penguin, agent, pixie, bear, bunny'}", clientid)
    except:
        send(f"Using: /spazall [AppearanceName] [or] /spaz [PlayerID] [AppearanceName] \n________________|_AppearanceName_|________________\n {'ali, wizard, cyborg, penguin, agent, pixie, bear, bunny'}", clientid)


def spazall(arguments, clientid):
 players = _ba.get_foreground_host_activity().players
 player = _ba.get_foreground_host_activity()
 a = arguments
 with ba.Context(player):
    for i in players:
        try:
            i.actor.node.color_texture = ba.gettexture(a[0]+"Color")
            i.actor.node.color_mask_texture = ba.gettexture(a[0]+"ColorMask")
            i.actor.node.head_model = ba.getmodel(a[0]+"Head")
            i.actor.node.torso_model = ba.getmodel(a[0]+"Torso")
            i.actor.node.pelvis_model = ba.getmodel(a[0]+"Pelvis")
            i.actor.node.upper_arm_model = ba.getmodel(a[0]+"UpperArm")
            i.actor.node.forearm_model = ba.getmodel(a[0]+"ForeArm")
            i.actor.node.hand_model = ba.getmodel(a[0]+"Hand")
            i.actor.node.upper_leg_model = ba.getmodel(a[0]+"UpperLeg")
            i.actor.node.lower_leg_model = ba.getmodel(a[0]+"LowerLeg")
            i.actor.node.toes_model = ba.getmodel(a[0]+"Toes")
            i.actor.node.style = a[0]
        except:
            send(f"Using: /spazall [AppearanceName] \n________________|_AppearanceName_|________________\n {'ali, wizard, cyborg, penguin, agent, pixie, bear, bunny'}", clientid)


def zombie(arguments, clientid):
 players = _ba.get_foreground_host_activity().players
 player = _ba.get_foreground_host_activity()
 a = arguments
 with ba.Context(player):
    try:
        try:
            if arguments != []:
                n = int(a[0])
            players[n].actor.node.color_texture = ba.gettexture("agentColor")
            players[n].actor.node.color_mask_texture = ba.gettexture("pixieColorMask")
            players[n].actor.node.head_model = ba.getmodel("zoeHead")
            players[n].actor.node.torso_model = ba.getmodel("bonesTorso")
            players[n].actor.node.pelvis_model = ba.getmodel("pixiePelvis")
            players[n].actor.node.upper_arm_model = ba.getmodel("frostyUpperArm")
            players[n].actor.node.forearm_model = ba.getmodel("frostyForeArm")
            players[n].actor.node.hand_model = ba.getmodel("bonesHand")
            players[n].actor.node.upper_leg_model = ba.getmodel("bonesUpperLeg")
            players[n].actor.node.lower_leg_model = ba.getmodel("pixieLowerLeg")
            players[n].actor.node.toes_model = ba.getmodel("bonesToes")
            players[n].actor.node.color = (0,1,0)
            players[n].actor.node.highlight = (0.6,0.6,0.6)
            players[n].actor.node.style = "spaz"
        except:
            send(f"Using: /zombieall [or] /zombie [PlayerID]", clientid)
    except:
        send(f"Using: /zombieall [or] /zombie [PlayerID]", clientid)


def zombieall(arguments, clientid):
 players = _ba.get_foreground_host_activity().players
 player = _ba.get_foreground_host_activity()
 a = arguments
 with ba.Context(player):
    for i in players:
        try:
            i.actor.node.color_texture = ba.gettexture("agentColor")
            i.actor.node.color_mask_texture = ba.gettexture("pixieColorMask")
            i.actor.node.head_model = ba.getmodel("zoeHead")
            i.actor.node.torso_model = ba.getmodel("bonesTorso")
            i.actor.node.pelvis_model = ba.getmodel("pixiePelvis")
            i.actor.node.upper_arm_model = ba.getmodel("frostyUpperArm")
            i.actor.node.forearm_model = ba.getmodel("frostyForeArm")
            i.actor.node.hand_model = ba.getmodel("bonesHand")
            i.actor.node.upper_leg_model = ba.getmodel("bonesUpperLeg")
            i.actor.node.lower_leg_model = ba.getmodel("pixieLowerLeg")
            i.actor.node.toes_model = ba.getmodel("bonesToes")
            i.actor.node.color = (0,1,0)
            i.actor.node.highlight = (0.6,0.6,0.6)
            i.actor.node.style = "spaz"
        except:
            send(f"Using: /zombieall [or] /zombie [PlayerID]", clientid)


def tex(arguments, clientid):
 players = _ba.get_foreground_host_activity().players
 player = _ba.get_foreground_host_activity()
 a = arguments
 with ba.Context(player):
    try:
        if len(a) > 1: n = int(a[0])
        color = None
        if (len(a) > 1) and (str(a[1]) == 'kronk'): color = str(a[1])
        else:color = str(a[1]) + 'Color'
        try:
            players[n].actor.node.color_mask_texture= ba.gettexture(str(a[1]) + 'ColorMask')
            players[n].actor.node.color_texture= ba.gettexture(color)
        except:
            send(f"Using: /texall [texture] [or] /tex [PlayerID] [texture]", clientid)
    except:
        send(f"Using: /texall [texture] [or] /tex [PlayerID] [texture]", clientid)


def texall(arguments, clientid):
 players = _ba.get_foreground_host_activity().players
 player = _ba.get_foreground_host_activity()
 a = arguments
 with ba.Context(player):
    try:
        color = None
        if str(a[0]) == 'kronk':
            color = str(a[0])
        else:color = str(a[0]) + 'Color'
        for i in players:
            try:
                i.actor.node.color_mask_texture= ba.gettexture(str(a[0]) + 'ColorMask')
                i.actor.node.color_texture= ba.gettexture(color)
            except:
                pass
    except:
        send(f"Using: /texall [texture] [or] /tex [PlayerID] [texture]", clientid)


def control(arguments, clientid):
 players = _ba.get_foreground_host_activity().players
 player = _ba.get_foreground_host_activity()
 a = arguments
 with ba.Context(player):
    try:
        if True:
            try:
                player1 = int(a[0])
            except:
                pass
            try:
                player2 = int(a[1])
            except:
                pass
        node1 = players[player1].actor.node
        node2 = players[player2].actor.node
        players[player1].actor.node = node2
        players[player2].actor.node = node1         
    except:
        send(f"Using: /exchange [PlayerID1] [PlayerID2]", clientid)
        

def icy(arguments, clientid):
 players = _ba.get_foreground_host_activity().players
 player = _ba.get_foreground_host_activity()
 a = arguments
 with ba.Context(player):
    try:
        if True:
            try:
                player1 = int(a[0])
            except:
                pass
            try:
                player2 = int(a[1])
            except:
                pass
        node1 = players[player2].actor.node
        players[player1].actor.node = node1         
    except:
        send(f"Using: /icy [PlayerID1] [PlayerID2]", clientid)
        
        
def play_ooh_sound(arguments):
  players = _ba.get_foreground_host_activity().players
  player = _ba.get_foreground_host_activity()
  with ba.Context(player):  
    try:
        a = arguments
        if a is not None and len(a) > 0:
            times = int(a[0])
            def ooh_recursive(c):
                ba.playsound(ba.getsound('ooh'), volume=2)
                c -= 1
                if c > 0:
                    ba.Timer(int(a[1]) if len(a) > 1 and a[1] is not None else 1000, ba.Call(ooh_recursive, c=c))
            ooh_recursive(c=times)
        else:
            ba.playsound(ba.getsound('ooh'), volume=2)
    except Exception as e:
        pass


def play_sound(arguments, clientid):
  players = _ba.get_foreground_host_activity().players
  player = _ba.get_foreground_host_activity()
  with ba.Context(player):  
    try:
        a = arguments  # Assign arguments to 'a'
        if a is not None and len(a) > 0:
            sound_name = str(a[0])
            times = int(a[1]) if len(a) > 1 else 1  # Set default times to 1 if not provided
            volume = float(a[2]) if len(a) > 2 else 2.0  # Set default volume to 2.0 if not provided
            def play_sound_recursive(c):
                ba.playsound(ba.getsound(sound_name), volume=volume)
                c -= 1
                if c > 0:
                    ba.Timer(int(a[3]) if len(a) > 3 and a[3] is not None else 1000, ba.Call(play_sound_recursive, c=c))
            play_sound_recursive(c=times)
        else:
            send(f"Using: /playsound [music sound] [time] [volume]", clientid)
    except Exception as e:
        send(f"Using: /playsound [music sound] [time] [volume]", clientid)
        
        
def acl(arguments, clientid):
         send(f"\ue046____________|ADMIN-CMDS-LISTS|______________\ue046", clientid)
         send(f"\ue046|| kick, kill, heal, curse, ooh, sleep, superpunch or sp,  gloves, tint", clientid)
         send(f"\ue046|| shield, ice, thaw, gm, playsound, inv, hl, speed, sm, dv, nv, creepy, ac", clientid)
         send(f"\ue046|| hug, tex, icy, celebrate, end, fly, lm, gp, remove, zombie, reflections", clientid)


def vcl(arguments, clientid):
         send(f"\ue046___________|VIP-CMDS-LISTS|______________\ue046", clientid)
         send(f"\ue046|| kill, heal, curse, sleep, ooh, gloves, creepy, hug, shield, thaw, fly", clientid)
         send(f"\ue046|| box, tex, inv, hl, zombie, playsound, nv, dv, sm, ice, lm, end, remove", clientid)


