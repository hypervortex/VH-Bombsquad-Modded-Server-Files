from .Handlers import handlemsg, handlemsg_all, send, clientid_to_myself, sendall, sendchat
from playersData import pdata
import discord, requests, asyncio
from features import discord_bot as dc
from stats import mystats
from ba._general import Call
# from tools.whitelist import add_to_white_list, add_commit_to_logs
from serverData import serverdata
from bastd.actor.spaz import Spaz
import ba
import _ba,os,json
import time
import setting
import ba.internal
import _thread
import random
from datetime import datetime, timedelta
from stats import mystats
from bastd.gameutils import SharedObjects
from tools import playlist
from tools import logger, mongo
Commands = ['hug', 'icy', 'spaz', 'top', 'setscore', 'disablebomb', 'zombieall', 'boxall', 'texall', 'kickall', 'ooh', 'spazall', 'acla', 'vcl', 'removepaidtag', 'complaint']
CommandAliases = ['cc', 'ccall', 'control', 'ooh', 'playsound', 'dbomb', 'resetstats', 'pme', 'zombie', 'rainbow', 'tex', 'hugall', 'box', 'ac', 'exchange', 'tint', 'say', 'playsound', 'admisncmdlist', 'vipcmdlist', 'rpt', 'comp']


def NewCommands(command, arguments, clientid, accountid, ARGUMENTS):
    """
    Checks The Command And Run Function
    Parameters:
        command : str
        arguments : str
        ARGUMENTS : str
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

    elif command == 'pme':
        fetch_send_stats(accountid, clientid, arguments)
        
    elif command in ['cc', 'spaz']:
        spaz(arguments, clientid)

    elif command in ['ccall', 'spazall']:
        spazall(arguments, clientid)

    # elif command in ['removepaideffect', 'rpe']:
    #     rpe(arguments, clientid, accountid)

    elif command in ['removepaidtag', 'rpt']:
        rpt(arguments, clientid, accountid)

    elif command == 'ac':
        ac(arguments, clientid)
        
    elif command == 'tint':
        tint(arguments, clientid)

    elif command == 'top':
        top(arguments, clientid)

    elif command in ['setscore', 'resetstats']:
        reset(arguments, clientid)

    elif command in ['dbomb', 'disablebomb']:
        dbomb(arguments, clientid)

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

    elif command in ['vcl', 'vipcmdlist']:
        vcl(arguments, clientid)

    elif command == 'ooh':
        play_ooh_sound(arguments)

    elif command == 'playsound':
        play_sound(arguments, clientid)     

    elif command in ['comp', 'complaint']:
        get_complaint(arguments, clientid, accountid, ARGUMENTS)  
 
    elif command == 'disco':
        start_disco(arguments)


def start_disco(arguments):
   players = _ba.get_foreground_host_activity().players
   player = _ba.get_foreground_host_activity()
   a = arguments
   with ba.Context(player):
    times = [0]

    # Define the colors for the disco effect
    colors = [
        (1, 0.6, 0.6),  # Red
        (0.6, 1, 0.6),  # Green
        (5, 1, 3),      # Pink
        (1, 6, 6),      # Light Blue
        (0.6, 0.6, 1)   # Blue
    ]

    # Create a light node for each color
    light_nodes = []
    for color in colors:
        light = ba.newnode('light',
                           owner=player.node,
                           attrs={'color': color,
                                  'radius': 0.1})
        light_nodes.append(light)

    def disco():
        # Calculate the color index based on time
        color_index = int((times[0] * 0.1) % len(colors))
        # Interpolate between the current color and the next color
        current_color = colors[color_index]
        next_color = colors[(color_index + 1) % len(colors)]
        t = (times[0] * 0.1) % 1
        new_color = (
            current_color[0] + (next_color[0] - current_color[0]) * t,
            current_color[1] + (next_color[1] - current_color[1]) * t,
            current_color[2] + (next_color[2] - current_color[2]) * t
        )
        # Apply the new color to the player's tint
        player.globalsnode.tint = new_color

        # Increment time
        times[0] += 1

        # Update the colors of the light nodes
        for i, light in enumerate(light_nodes):
            light_color = colors[(color_index + i) % len(colors)]
            light.color = light_color

        # Call disco function again after a short delay
        ba.timer(33, disco)

    # Start the disco effect
    disco()

          
def dbomb(arguments, clientid):
    print("Command received: /dbomb")
    settings = setting.get_settings_data()
    print("Current bomb count:", settings['playermod']['default_bomb_count'])
    
    if arguments == [] or arguments == ['']:
        if settings['playermod']['default_bomb_count'] != 0:
            settings['playermod']['default_bomb_count'] = 0
            setting.commit(settings)
            print("Settings after disabling bombs:", setting.get_settings_data())  # Print updated settings
            ba.internal.chatmessage("Bombs are disabled now :(")
            send("To turn on bombs, type /dbomb", clientid)
        else:
            settings['playermod']['default_bomb_count'] = 2
            setting.commit(settings)
            print("Settings after enabling bombs:", setting.get_settings_data())  # Print updated settings
            ba.internal.chatmessage("Now you can use bombs :)")


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

            
def stats_clientid(ac_id, clientid, arguments):
 session = ba.internal.get_foreground_host_session()   
 if arguments == [] or arguments == ['']:    
      for i in session.sessionplayers:
          if i.inputdevice.client_id == int(arguments[0]):    
              acid = i.get_v1_account_id()
              stats = mystats.get_stats_by_id(acid)
              if stats:
                 tickets = getcoins(acid)
                 reply = (
                     f"\ue048| Name: {stats['name']}\n"
                     f"\ue048| PB-ID: {stats['aid']}\n"
                     f"\ue048| Tickets: {tickets}\ue01f\n"
                     f"\ue048| Rank: {stats['rank']}\n"
                     f"\ue048| Score: {stats['scores']}\n"
                     f"\ue048| Games: {stats['games']}\n"
                     f"\ue048| Kills: {stats['kills']}\n"
                     f"\ue048| Deaths: {stats['deaths']}\n"
                     f"\ue048| Avg.: {stats['avg_score']}\n"
                  )
              else:
                  reply = "Not played any match yet."

              _ba.pushcall(Call(send, reply, clientid), from_other_thread=True)


def fetch_send_stats(ac_id, clientid, arguments):
    _thread.start_new_thread(stats_clientid, (ac_id, clientid, arguments,))   
 
        
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
        
#REMOVE PAID EFFECT
# def rpe(arguments, clientid, accountid):
#     try:
#         custom = pdata.get_custom()['paideffects']
#         aeffect = custom[accountid]['effect']
#         session = ba.internal.get_foreground_host_session()
#         for i in session.sessionplayers:
#             if i.inputdevice.client_id == int(arguments[0]):
#                 pdata.remove_paid_effect(i.get_v1_account_id())
#                 send(f"paid {aeffect} effect have been removed Successfully", clientid)
#     except:
#         return

#REMOVE PAID TAG
def rpt(arguments, clientid, accountid):
    try:
        custom = pdata.get_custom()['paidtags']
        atag = custom[accountid]['tag']
        session = ba.internal.get_foreground_host_session()
        for i in session.sessionplayers:
            if i.inputdevice.client_id == int(arguments[0]):
                pdata.remove_paid_tag(i.get_v1_account_id())
                send(f"paid {atag} tag have been removed Successfully", clientid)
    except:
        return

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


def acl(arguments, clientid):
         data = pdata.roles_cmdlist(admin)
         send(f"\ue046____________|ADMIN-CMDS-LISTS|______________\ue046", clientid)
         send(f"\ue046|| {data} kick, kill, heal, curse, sleep, superpunch or sp,  gloves, tint", clientid)
         send(f"\ue046|| shield, ice, thaw, gm, fly, inv, hl, speed, sm, dv, nv, creepy, ac", clientid)
         send(f"\ue046|| hug, tex, icy, celebrate, end, lm, gp, remove, zombie, reflections", clientid)


def vcl(arguments, clientid):
         send(f"\ue046___________|VIP-CMDS-LISTS|______________\ue046", clientid)
         send(f"\ue046|| kill, heal, curse, sleep, gloves, hug, shield, ice, thaw, fly", clientid)
         send(f"\ue046|| box, tex, inv, hl, zombie, creepy, nv, dv, sm, lm, end, remove", clientid)


def top(arguments, clientid, id):
 players = _ba.get_foreground_host_activity().players
 player = _ba.get_foreground_host_activity()
 a = arguments
 base_path = os.path.join(_ba.env()['python_directory_user'], "stats" + os.sep)
 statsFile = base_path + 'stats.json'
 with ba.Context(player):
     try:
         temp_limit = int(a[0])
         temp_toppers = []
         f = open(statsFile, 'r')
         temp_stats = mystats.get_all_stats()
         for i in range(1,limit+1):
             for id in temp_stats:
                 if int(temp_stats[id]['rank'])==i: temp_toppers.append(id)
         if temp_toppers != []:
             for account_id in temp_toppers:
                 temp_name = temp_stats[accountid]['name']
                 _ba.chatmessage("{0}. {1}  ----->  {2}".format(temp_toppers.index(account_id)+1,temp_name[temp_name.find('>')+1:].encode('utf8'),temp_stats[account_id]['scores']))
         f.close()
     except:
         send(f"Usage: /top <range>", clientid)      


def reset(arguments, clientid):
 players = _ba.get_foreground_host_activity().players
 player = _ba.get_foreground_host_activity()
 a = arguments
 base_path = os.path.join(_ba.env()['python_directory_user'], "stats" + os.sep)
 statsFile = base_path + 'stats.json'
 with ba.Context(player):
   try:
       temp_rank = int(a[0])
       temp_stats = mystats.get_all_stats()
       for id in temp_stats:
           if id['client_id'] == temp_stats:
              if int(temp_stats[id]['rank']) == temp_rank: accountid = id
       f.close()
       temp_name = temp_stats[accountid]['name']
       temp_name = temp_name[temp_name.find('>')+1:].encode('utf-8')
       try:
           temp_score = int(a[1])
       except:
           temp_score = 0
       stats[accountid]['score'] = temp_score
       _ba.chatmessage("{}'s score set to {}".format(temp_name,temp_score))
       #backup
       from shutil import copyfile
       src = statsFile
       from datetime import datetime
       now = datetime.now().strftime('%d-%m %H:%M:%S')
       dst = 'stats.bak---' + now
       copyfile(src,dst)
       #write new stats
       f = open(statsFile, 'w')
       f.write(json.dumps(temp_stats))
       f.close()
       '''
       mystats.refreshStats()
       '''
   except:
       send(f"Usage: /reset <rank of player> (optional:newScore)", clientid)

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


def get_complaint(arguments, clientid, acid, ARGUMENTS):
    players = _ba.get_foreground_host_activity().players
    player = _ba.get_foreground_host_activity()
    server = _ba.app.server._config.party_name
    customers = pdata.get_custom()['complainter']
    a = arguments
    b = ARGUMENTS
    
    if not arguments or arguments == ['']:
        with ba.Context(player):
            send(f"Using: /comp [Clientid of offender] [complaint reason]", clientid)
    else:
        cl_id = int(arguments[0])
        complaint = " ".join(b[1:])
        
        # Check if the user is trying to complain against themselves
        if cl_id == clientid:
            send("You can't file a complaint against yourself.", clientid)
            return

        for pla in ba.internal.get_foreground_host_session().sessionplayers:
            if pla.inputdevice.client_id == clientid:
                name = pla.getname(full=True, icon=True)
            if pla.inputdevice.client_id == cl_id:
                fname = pla.getname(full=True, icon=True)

        for ros in ba.internal.get_game_roster():
            if ros['account_id'] == acid:
                myself = ros["display_string"]

        for roe in ba.internal.get_game_roster():
            if roe["client_id"] == cl_id:
                offendr = roe["display_string"]
                pbid = roe["account_id"]
                otheraccounts = pdata.get_detailed_pinfo(pbid)
                
                now = datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')
                
                if acid not in customers:
                    if not complaint:
                        send("Please provide a complaint reason.", clientid)
                        return
                    
                    expiry = datetime.now() + timedelta(seconds=30)
                    customers[acid] = {'expiry': expiry.strftime('%d-%m-%Y %I:%M:%S %p')}
                    
                    # Call the send_complaint_to_channel function                
                    asyncio.ensure_future(dc.send_complaint_to_channel(server_name=server, time=now, myself=myself, ign=name, useracid=acid, fign=fname, acid=pbid, linkedaccount=otheraccounts, offender=offendr, complaint=complaint))
                    
                    send("A complaint has been sent on the Discord server. Please wait for Staff to take action...!!", clientid)
                else:
                    till = customers[acid]['expiry']
                    send(f"You can use the complaint command again at {till}", clientid)
      
