# ADVANCED LOGGING BOT SYSTEM BY VORTEXXXXXX & ROCKY
from re import A
import discord, requests, asyncio ,ba, _ba, ba.internal, json, psutil, _thread
from threading import Thread
from discord.ext.commands import Bot
from ba._general import Call
from playersData import pdata
from serverData import serverdata
import setting
from tools import mongo
from chatHandle.ChatCommands.commands import NormalCommands as nc
from chatHandle.ChatCommands.commands import CoinCmds as cc
from bacommon.servermanager import ServerConfig
from features import complaints as c
import members.members as mid
import datetime
from stats import mystats
import os
intents = discord.Intents().all()
client = Bot(command_prefix='v!', intents=intents)

stats = {}
livestatsmsgs = []
logsChannelID = 859519868838608970
liveStatsChannelID = 1079019991694839818
whitelisted_servers = 1168272029280112673
whitelisted_users = 123456789012345678
Notify_channel_id=1209532711673528413
complaintChannelID=1209532711673528413
prefix = ''
commands_prefix = ''
liveChat = True
token = ''
logs = []
current_directory = os.path.dirname(os.path.abspath(__file__))
setting_json_path = os.path.join(current_directory, '..', 'setting.json')
BANK_PATH = _ba.env().get("python_directory_user", "") + "/bank.json"



def push_log(msg):
    global logs
    logs.append(msg)

def init():
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(token))
    Thread(target=loop.run_forever).start()

def addcoins(accountid: str, amount: int):
    if os.path.exists(BANK_PATH):
        with open(BANK_PATH) as f:
            bank = json.loads(f.read())
    else:
        bank = {}
    if accountid not in bank:
        bank[accountid] = 0
    bank[accountid] += amount
    with open(BANK_PATH, 'w') as f:
        f.write(json.dumps(bank))
    if amount > 0:
      print('Transaction successful')
      
def removecoins(accountid: str, amount: int):
    if os.path.exists(BANK_PATH):
        with open(BANK_PATH) as f:
            bank = json.loads(f.read())
    else:
        bank = {}
    if accountid not in bank:
        bank[accountid] = 0
    bank[accountid] -= amount
    with open(BANK_PATH, 'w') as f:
        f.write(json.dumps(bank))
    if amount > 0:
      print('Transaction successful')
      
channel = None

async def send_message_chunks(channel, messages):
    max_message_length = 2000
    chunks = [messages[i:i+max_message_length] for i in range(0, len(messages), max_message_length)]
    for chunk in chunks:
        await channel.send("".join(chunk))

async def send_complaint_to_channel(server_name, time, myself, ign, useracid, fign, acid, linkedaccount, offender, complaint):
    # Replace YOUR_COMPLAINTS_CHANNEL_ID with the actual ID of your complaints channel
    #channel_id = 1079019994802827284
    channel = client.get_channel(complaintChannelID)

    if not channel:
        print(f"Channel with ID {complaintChannelID} not found.")
        return
    
    complaint_message = (
        f":reminder_ribbon:**__{server_name}__\n=========================================**\n> |:arrow_right:`COMPLAINT TIME:` {time}\n> \n> |:arrow_right:`USERNAME(IGN)/ACCOUNT-ID:` {myself} ({ign})/{useracid}\n> \n"
        f"> |:arrow_right:`OFFENDER(IGN)/ACCOUNT-ID:` {offender} ({fign})/{acid}\n> \n> |:arrow_right:`LINKED-ACCOUNTS OF OFFENDER:` {linkedaccount}\n> \n> |:arrow_right:`TYPE OF COMPLAINT:` **{complaint}**\n> __<@&1079030765733556334> <@&1073263867251134594>__\n**=========================================**"
    )
    c.update_complaint_count(useracid, myself, mongo)
    c.update_complaints_count(acid, offender, mongo)
    await channel.send(complaint_message)    


async def joined_player(pbid, devices_string, time):
    # Replace YOUR_NOTIFY_CHANNEL_ID with the actual ID of your complaints channel
    #Notify_channel_id = 1201908867810730034
    channel = client.get_channel(Notify_channel_id)
    otheraccounts = pdata.get_detailed_pinfo(pbid)
    serverss = _ba.app.server._config.party_name

    if not channel:
        print(f"Channel with ID {Notify_channel_id} not found.")
        return
    
    message = (
        f":reminder_ribbon:**__{serverss}__\n=========================================**\n> |:arrow_right:`PLAYER JOINED TIME:` {time}\n> \n> |:arrow_right:`PLAYER-NAME:` {devices_string}\n> \n"
        f"> |:arrow_right:`PLAYER ACCOUNT-ID:` {pbid}\n> \n> |:arrow_right:`LINKED-ACCOUNTS OF PLAYER:` {otheraccounts}\n> \n> |:arrow_right:**JOINED THE GAME**\n> __ <@&1207249247460659210> __\n**=========================================**"
    )
    await channel.send(message)
    #print(f"{devices_string}... Notification send Successfully!")

def log_command(user_id, user_name, command):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    logs_data = pdata.get_DiscordCmds()
    
    logs_data.append({
        "user_id": user_id,
        "user_name": user_name,
        "command": command,
        "timestamp": timestamp
    })
    
    # Update logs data
    pdata.update_DiscordCmdLogs()
    
@client.event
async def on_message(message):
    global channel
    if message.author == client.user:
        return
    channel = message.channel

    if message.channel.id == logsChannelID:
        _ba.pushcall(Call(ba.internal.chatmessage, message.content), from_other_thread=True)
    else:    
        if message.content.startswith(prefix):
            if message.guild.id not in whitelisted_servers:
                print(f"Server ID {message.guild.id} is not whitelisted.Someone is trying to use {client.user.name} in other servers")
                try:
                    guild = client.get_guild(message.guild.id)
                    server_name = guild.name if guild else "Unknown Server"
                    print(f"Unauthorized attempt in server: {server_name}")
                except Exception as e:
                    print(f"Error retrieving server name: {e}")
                await message.channel.send("**Unauthorized server. This server is not whitelisted. Don't try to use cmds kid...!**")
                return

            if message.author.id not in whitelisted_users:
                await message.channel.send("**You do not have permission to use this command.**")
                return

            cmd = commands_prefix            
           # user_id = message.author.id
           # user_name = message.author.name
            #command = m[0]
            #incomeplete, it has some errors fix if u can (so basically its logs dc cmd in json file)
            #log_command(message.author.id, message.author.name, message.content)  
            servers = _ba.app.server._config.party_name
            m = message.content[2:].split()
            if m[0] == 'bsunban': #unban in all server xD
                if len(m) == 2:
                    pb_id_to_unban = m[1]                	
                    banned = mongo.Banlist.find_one() or {'ban': {'ids': [], 'deviceids': [], 'ips': []}}

                    if pb_id_to_unban in banned['ban']['ids']:
                        index = banned['ban']['ids'].index(pb_id_to_unban)
                        device_id = banned['ban']['deviceids'][index]
                        ip_address = banned['ban']['ips'][index]

                        banned['ban']['ids'].remove(pb_id_to_unban)
                        banned['ban']['deviceids'].pop(index)
                        banned['ban']['ips'].pop(index)

                        mongo.Banlist.delete_many({})
                        mongo.Banlist.insert_one(banned)

                        await message.channel.send(f">>> :arrow_right:**Successfully unbanned `{pb_id_to_unban}` in all servers **")
                    else:
                        await message.channel.send(">>> :arrow_right:**`I can't find that PB-ID in my database`** 😕!")
                else:
                    await message.channel.send(">>> :arrow_right:<a:wrong:1178654358896910449>**Invalid Format! Use `{0}bsunban <pbid>`**".format(prefix))

            # quit in all server :))))))
            elif m[0] == 'quit': 
                await message.channel.send(">>> :arrow_right:**<a:correct:1178796582334898326>`Successfully restarted all servers` **")                  
                ba.quit()

            # add player data whom notify you want in Discord server xD
            elif m[0] == 'addnotify':
                if len(m) == 4:
                    data = mongo.notify_list.find_one() or {'notify': {'ids': [], 'deviceids': [],'ips': []}}
                    player_id = m[1]
                    device_id = m[2]
                    ip = m[3]

                    if player_id not in data['notify']['ids'] and device_id not in data['notify']['deviceids'] and ip not in data['notify']['ips']: # Use get method to handle potential missing key     
                        data['notify']['ids'].append(player_id)                            
                        data['notify']['deviceids'].append(device_id)
                        data['notify']['ips'].append(ip)      
                        mongo.notify_list.delete_many({}) # Move the update_notify call inside the condition      
                        mongo.notify_list.insert_one(data)    
                        await message.channel.send(f">>> :arrow_right:**Successfully added Player ID {player_id} in the Notify list**")
                    else:
                        await message.channel.send(f">>> :arrow_right:**Player ID {player_id} is already in the Notify list**")                   
                else:
                    await message.channel.send(">>> :arrow_right::x:**Invalid Format! Use `{0}addnotify <pbid> <device_id> <ip>`**".format(prefix))       

            # remove account ID of a player you don't want to notify in the DC server :)                  
            elif m[0] == 'removenotify':
                if len(m) == 2:
                    player_id = m[1]
                    data = mongo.notify_list.find_one() or {'notify': {'ids': [], 'deviceids': [],'ips': []}}

                    if player_id in data['notify']['ids']:
                        index = data['notify']['ids'].index(player_id)
                        device_id = data['notify']['deviceids'][index]
                        ip = data['notify']['ips'][index]

                        data['notify']['ids'].remove(player_id)
                        data['notify']['deviceids'].pop(index)
                        data['notify']['ips'].pop(index)
                        mongo.notify_list.delete_many({})
                        mongo.notify_list.insert_one(data)
                        await message.channel.send(f">>> :arrow_right:**Successfully Removed Player ID {player_id} from the Notify list**")
                    else:
                        await message.channel.send(f">>> :arrow_right:**Player ID {player_id} is not in the Notify list**")
                else:
                    await message.channel.send(">>> :arrow_right::x:**Invalid Format! Use `{0}removenotify <pbid>`**".format(prefix))

            #to check if player is there in notify list or not :)
            elif m[0] == 'checknotify':
                data = mongo.notify_list.find_one() or {'notify': {'ids': [], 'deviceids': [],'ips': []}}
                if data and 'notify' in data:
                    notify_ids = data['notify']['ids']
                    notify_device_ids = data['notify']['deviceids']
                    notify_ips = data['notify']['ips']

                    if len(m) == 2: 
                        pb_id_to_check = m[1]
                        if pb_id_to_check in notify_ids:
                            index = notify_ids.index(pb_id_to_check)
                            device_id = notify_device_ids[index]
                            ip = notify_ips[index]
                            await message.channel.send(f">>> :arrow_right:**Player with PB-ID `{pb_id_to_check}` is in the notify list**")
                        else:
                            await message.channel.send(f">>> :arrow_right:**Player with PB-ID `{pb_id_to_check}` is not found in the notify list**")
                    else:
                        await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}checknotify <pbid>`**".format(prefix))

            # to find out how many complaint does the user have done :))
            elif m[0] == 'complain':
                complain = mongo.complaint_count.find_one() or {'complainter': {'pb_id': [], 'name': [], 'count': []}}
                if complain and 'complainter' in complain:
                    complain_ids = complain['complainter']['pb_id']
                    complain_name = complain['complainter']['name']
                    complain_count = complain['complainter']['count']

                    if len(m) == 2: 
                        pb_id_to_check = m[1]
                        if pb_id_to_check in complain_ids:
                            index = complain_ids.index(pb_id_to_check)
                            name = complain_name[index]
                            count = complain_count[index]
                            complain_message = (
                                f"> |:arrow_right:`PLAYER-NAME:` {name}\n> |:arrow_right:`PLAYER PB-ID:` {pb_id_to_check}\n> |:arrow_right:`COMPLAIN COUNT:` {count}"
                            )                                 
                            await message.channel.send(complain_message)
                        else:
                            await message.channel.send(f">>> :arrow_right:**`Player with PB-ID {pb_id_to_check} hasn't submitted any complaints so far.`**")
                    else:
                        await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}complain <pbid>`**".format(prefix))

            # to find out how many complaints does this user have xD
            elif m[0] == 'complaints':
                complaints = mongo.complaints_count.find_one() or {'complaints': {'pb_id': [], 'name': [], 'count': []}}
                if complaints and 'complaints' in complaints:
                    complaints_ids = complaints['complaints']['pb_id']
                    complaints_name = complaints['complaints']['name']
                    complaints_count = complaints['complaints']['count']

                    if len(m) == 2: 
                        pb_id_to_check = m[1]
                        if pb_id_to_check in complaints_ids:
                            index = complaints_ids.index(pb_id_to_check)
                            name = complaints_name[index]
                            count = complaints_count[index]
                            complaints_message = (
                                f"> |:arrow_right:`PLAYER-NAME:` {name}\n> |:arrow_right:`PLAYER PB-ID:` {pb_id_to_check}\n> |:arrow_right:`COMPLAINTS COUNT:` {count}"
                            )                                 
                            await message.channel.send(complaints_message)
                        else:
                            await message.channel.send(f">>> :arrow_right:**`Player with PB-ID {pb_id_to_check} hasn't received any complaints yet.`**")
                    else:
                        await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}complaints <pbid>`**".format(prefix))

           #check last 15 complain players :D
            elif m[0] == 'complainlist':
                    complain = mongo.complaint_count.find_one() or {'complainter': {'pb_id': [], 'name': [], 'count': []}}
                    if complain and 'complainter' in complain:
                        complain_ids = complain['complainter']['pb_id']
                        complain_name = complain['complainter']['name']
                        complain_count = complain['complainter']['count']

                        if complain_ids:
                            complain_messages = [
                                f">>> :reminder_ribbon: **Last 15 Complain Players ({len(complain_ids)}):**"
                            ]

                            start_index = max(0, len(complain_ids) - 15)
                            for i in range(start_index, len(complain_ids)):
                                pbid = complain_ids[i]
                                name = complain_name[i]
                                count = complain_count[i]
                                complain_messages.append(f":arrow_right:**PB-ID: `{pbid}`, Name: `{name}`, Complain Count: `{count}`**")

                            await message.channel.send("\n".join(complain_messages))
                        else:
                            await message.channel.send(":arrow_right:**`No players are currently complain.`**")
                    else:
                        await message.channel.send(":arrow_right:**No complain data found.**")

           #check last 15 complaints players :D
            elif m[0] == 'complaintslist':
                    complaints = mongo.complaints_count.find_one() or {'complaints': {'pb_id': [], 'name': [], 'count': []}}
                    if complaints and 'complaints' in complaints:
                        complaints_ids = complaints['complaints']['pb_id']
                        complaints_name = complaints['complaints']['name']
                        complaints_count = complaints['complaints']['count']

                        if complaints_ids:
                            complaints_messages = [
                                f">>> :reminder_ribbon: **Last 15 Complaints Players ({len(complaints_ids)}):**"
                            ]

                            start_index = max(0, len(complaints_ids) - 15)
                            for i in range(start_index, len(complaints_ids)):
                                pbid = complaints_ids[i]
                                name = complaints_name[i]
                                count = complaints_count[i]
                                complaints_messages.append(f":arrow_right:**PB-ID: `{pbid}`, Name: `{name}`, Complaints Count: `{count}`**")

                            await message.channel.send("\n".join(complaints_messages))
                        else:
                            await message.channel.send(":arrow_right:**`No players are currently complaints.`**")
                    else:
                        await message.channel.send(":arrow_right:**No complaints data found.**")
                        
            #cmds guide :)
            elif m[0] == 'help':
                help_messages = [
                    f">>> ## **:scroll:__COMMANDz GUIDE__ :) ** \n### __(To find out server code type {prefix}sc) __",
                    f":arrow_right:**__Banning and Unbanning:__**\n:arrow_right:Type `{prefix}ban` to learn how to ban and unban a player.",
                    f":arrow_right:**__Muting and Unmuting:__**\n:arrow_right:Type `{prefix}mute` to understand how to mute and unmute a player.",
                    f":arrow_right:**__Create & Remove Role and Change Role tag Commands:__**\n:arrow_right:Type `{prefix}createrole` to find out how to create & remove role and change role tag.",
                    f":arrow_right:**__Adding and Removing Roles:__**\n:arrow_right:Type `{prefix}addroles` to discover how to add and remove roles from a player.",
                    f":arrow_right:**__Remove Roles and Custom ID's:__**\n:arrow_right:Type `{prefix}removeids` to find out how to remove ID's from roles and customs.",  
                    f":arrow_right:**__Adding and Removing Commands from Roles:__**\n:arrow_right:Type `{prefix}addcmds` to find out how to add and remove commands from a role.",
                    f":arrow_right:**__Kick and Kick-vote Commands:__**\n:arrow_right:Type `{prefix}kickcmd` to find out how to use kick and kick vote cmds.",
                    f":arrow_right:**__Sending Messages in Servers:__**\n:arrow_right:Type `{prefix}msg` to learn how to send messages in servers.",
                    f":arrow_right:**__Custom Tags and Effects:__**\n:arrow_right:Type `{prefix}customs` to know how to add and remove custom tags or effects from a player.",
                    f":arrow_right:**__Checking Player Data:__**\n:arrow_right:Type `{prefix}checkdata` to view all data related to a player.",
                    f":arrow_right:**__Change Stats Data:__**\n:arrow_right:Type `{prefix}csdata` to know how to change statsdata of a player."                             
                    ]
                await message.channel.send("\n".join(help_messages))
                help_message = [
                    f">>> :arrow_right:**__List and Count of Roles in Server:__**\n:arrow_right:Type `{prefix}roleslc` to see the list and count of roles in the server.",  
                    f":arrow_right:**__ Notifications and Complaint Commands:__**\n:arrow_right:Type `{prefix}nac` to learn about notification and complaint commands.",                
                    f":arrow_right:**__Restarting (Quitting) the Server:__**\n:arrow_right:Type `{prefix}restart` to understand how to restart or quit the server.",
                    f":arrow_right:**__Adding Users to Whitelist:__**\n:arrow_right:Type `{prefix}user` to learn how to add a user to the whitelist, allowing them to use all bot commands."
                    ] 
                await message.channel.send("\n".join(help_message))
                
            elif m[0] == 'ban': 
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__BAN AND UNBAN COMMANDz:__**\n:arrow_right:`{prefix}bsban (pbid) (deviceid) (ip)` - To ban a player in all servers.\n:arrow_right:`{prefix}bsunban (pbid)` - To unban a player from all servers.\n:arrow_right:`{prefix}(server-code)ban (pbid) (time in days) (reason no space)` - To ban a player in a specific server.\n:arrow_right:`{prefix}(server-code)unban (pbid)` - To unban a player from a specific server. ")

            elif m[0] == 'mute': 
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__MUTE AND UNMUTE COMMANDz:__**\n:arrow_right:`{prefix}bsmute (pbid) (time in minutes) (reason no space)` - To mute a player in all servers.\n:arrow_right:`{prefix}bsunmute (pbid)` - To unmute a player from all servers.\n:arrow_right:`{prefix}(server-code)mute (pbid) (time in minutes) (reason no space)` - To mute a player in a specific server.\n:arrow_right:`{prefix}(server-code)unmute (pbid)` - To unmute a player from a specific server. ")

            elif m[0] == 'createrole': 
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__CREATE & REMOVE ROLE AND CHANGE ROLE TAG COMMANDz:__**\n:arrow_right:`{prefix}cr (role) (tag)` - To create a role and add roles tag in all servers.\n:arrow_right:`{prefix}rr (role) ` - To remove a role from all servers.\n:arrow_right:`{prefix}(server-code)cr (role) (tag)` - To create a role and add roles tag in a specific server.\n:arrow_right:`{prefix}(server-code)rr (role)` - To remove a role from a specific server.\n:arrow_right:`{prefix}crt (role) (tag)` - To change roles tag in all servers.\n:arrow_right:`{prefix}(server-code)crt (role) (tag)` - To change roles tag in a specific server. ")

            elif m[0] == 'addroles': 
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__ADDROLES COMMANDz:__**\n:arrow_right:`{prefix}addrole (pbid) (role)` - To add any role to a player in all servers.\n:arrow_right:`{prefix}removerole (pbid) (role)` - To remove any role from a player in all servers.\n:arrow_right:`{prefix}(server-code)addrole (pbid) (role)` - To add any role to a player in a specific server.\n:arrow_right:`{prefix}(server-code)removerole (pbid) (role)` - To remove any role from a player in a specific server. ")

            elif m[0] == 'addcmds': 
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__ADDCMD TO ROLE COMMANDz:__**\n:arrow_right:`{prefix}asac (role) (command)` - To add command in any role in all servers.\n:arrow_right:`{prefix}asrc (role) (command)` - To remove command from any role in all servers.\n:arrow_right:`{prefix}(server-code)ac (role) (command)` - To add command in any role in a specific server.\n:arrow_right:`{prefix}(server-code)rc (role) (commamd)` - To remove command from any role in a specific server. ")

            elif m[0] == 'msg': 
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__MSG COMMANDz:__**\n:arrow_right:`{prefix}im (server-name) (message)` - To send important message in all servers in one click....!\n:arrow_right:`{prefix}(server-code)im (server-name) (message)` - To send important message in a specific server. ")
    
            elif m[0] == 'customs':
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__CUSTOMTAG AND EFFECT COMMANDz:__**\n:arrow_right:`{prefix}(server-code)tagadd (pbid) (tag)` - To add customtag to player in a specific server.\n:arrow_right:`{prefix}(server-code)tagremove (pbid)` - To remove customtag from a player in a specific server.\n:arrow_right:`{prefix}tagadd (pbid) (tag)` - To add customtag to player in all servers.\n:arrow_right:`{prefix}tagremove (pbid)` - To remove customtag from a player in all servers.\n:arrow_right:`{prefix}(server-code)effectadd (pbid) (effect)` - To add customeffect to player in a specific server.\n:arrow_right:`{prefix}(server-code)effectremove (pbid)` - To remove customeffect from a player in a specific server.\n:arrow_right:`{prefix}effectadd (pbid) (effect)` - To add customeffect to player in all servers.\n:arrow_right:`{prefix}effectremove (pbid)` - To remove customeffect from a player in all servers.")

            elif m[0] == 'removeids':
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__REMOVE ROLES & CUSTOMS ID'S COMMANDz:__**\n:arrow_right:`{prefix}(server-code)rids (role)` - To remove roles all ID's from specific server.\n:arrow_right:`{prefix}rids (role)` - To remove rolea all ID's from all servers.\n:arrow_right:`{prefix}(server-code)rcids (custom)` - To remove customs all ID's from specific server.\n:arrow_right:`{prefix}rcids (custom)` - To remove customs all ID's from all servers. ")

            elif m[0] == 'checkdata':
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__CHECK ALL DATA COMMANDz:__**\n:arrow_right:`{prefix}bancheck (pbid)` - Check if a player is banned or unbanned in all servers.\n:arrow_right:`{prefix}(server-code)bancheck (pbid)` - Check if a player is banned or unbanned in a specific server.\n:arrow_right:`{prefix}getroles (pbid)` - Get info about the number of roles a player has across all servers.\n:arrow_right:`{prefix}(server-code)getroles (pbid)` - Get info about the number of roles a player have in a specific server.\n:arrow_right:`{prefix}(server-code)checktag (pbid)` - Check if a player has a custom tag in a specific server.\n:arrow_right:`{prefix}(server-code)checkeffect (pbid)` - Check if a player has a custom effect in a specific server.\n:arrow_right:`{prefix}(server-code)pdata (pbid)` - View a player's data (score, rank etc) on the specific server.\n:arrow_right:`{prefix}(server-code)bandata (pbid)` - View a player's ban data (ip, device-id etc) on the specific server.\n:arrow_right:`{prefix}(server-code)top10` - View the Top 10 players in the specific server.\n:arrow_right:`{prefix}(server-code)recents (limit)` - To Know Recently joined players in the specific server.\n:arrow_right:`{prefix}(server-code)lm (limit)` - To know all last messages of specific server.\n:arrow_right:`{prefix}(server-code)plm (pbid) (limit)` - To know player last messages of specific server.\n:arrow_right:`{prefix}(server-code)mp (count)` - To do Maximum player set in the specific server. ")

            elif m[0] == 'csdata':
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__CHANGE ANY STATS-DATA COMMANDz:__**\n:arrow_right:`{prefix}addcoins (pbid) (count)` - Add coins to a player in all servers.\n:arrow_right:`{prefix}removecoins (pbid) (count)` - Remove coins from player in all servers.\n:arrow_right:`{prefix}(server-code)addcoins (pbid) (count)` - Add coins to a player in a specific server.\n:arrow_right:`{prefix}(server-code)removecoins (pbid) (count)` - Remove coins from player in specific server.\n:arrow_right:`{prefix}(server-code)csd (pbid) (statsdata to change) (count)` - Change (statsdata) of a player in a specific server.\n:arrow_right:Use statsdata - `scores, kills, deaths, games, kd`")

            elif m[0] == 'kickcmd':
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__KICK AND KICK-VOTE COMMANDz:__**\n:arrow_right:`{prefix}(server-code)kick (pbid)` - To kick in-game player from a specific server.\n:arrow_right:`{prefix}dkickvote (pbid) (time in days) (reason no space)` - To disable server kick-vote for a player in all servers.\n:arrow_right:`{prefix}ekickvote (pbid)` - To enable server kick-vote for a player in all servers.\n:arrow_right:`{prefix}(server-code)dkickvote (pbid) (time in days) (reason no space)` - To disable server kick-vote for a player in a specific server.\n:arrow_right:`{prefix}(server-code)ekickvote (pbid)` - To enable server kick-vote for a player in a specific server.")

            elif m[0] == 'roleslc':
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__LIST & COUNT COMMANDz:__**\n:arrow_right:`{prefix}mbanlist` - Ascertain last 10 banned players of all servers.\n:arrow_right:`{prefix}(server-code)banlist` - Ascertain last 10 banned players of specific server.\n:arrow_right:`{prefix}complainlist` - Ascertain last 15 complain players & counts.\n:arrow_right:`{prefix}complaintslist` - Ascertain last 15 complaints players & counts.\n:arrow_right:`{prefix}(server-code)mutelist` - Find out muted players of specific server.\n:arrow_right:`{prefix}(server-code)roleslist` - Find out all roles of specific server.\n:arrow_right:`{prefix}(server-code)dkickvotelist` - Find out disable server kick-vote players of specific server.\n:arrow_right:`{prefix}(server-code)viplist` - Find out VIPs list & count of specific server.\n:arrow_right:`{prefix}(server-code)adminlist` - Find out Admins list & count of specific server.\n:arrow_right:`{prefix}(server-code)cslist` - Find out CS list & count of specific server.\n:arrow_right:`{prefix}(server-code)modlist` - Find out Moderators list & count of specific server.\n:arrow_right:`{prefix}(server-code)leadstafflist` - Find out Leadstaff list & count of specific server.\n:arrow_right:`{prefix}(server-code)ownerlist` - Find out Owners list & count of specific server.\n:arrow_right:`{prefix}(server-code)taglist` - Find out CustomTag players list & count of specific server.\n:arrow_right:`{prefix}(server-code)effectlist` - Find out CustomEffect players list & count of specific server.\n:arrow_right:`{prefix}(server-code)cmdlist <role>` - Find out Roles Cmdlist of specific server.\n:arrow_right:`{prefix}aeffectlist` - Find out Available CustomEffects list of all servers. ")

            elif m[0] == 'nac':
                await message.channel.send(f">>> :arrow_right:**__NOTIFICATIONS AND COMPLAINT COMMANDz:__**\n:arrow_right:`{prefix}addnotify (pbid) (deviceid) (ip)` - To add the player in the notification list.\n:arrow_right:`{prefix}removenotify (pbid)` - To remove the player from the notification list.\n:arrow_right:`{prefix}checknotify (pbid)` - Verify whether the player is included in the notification list or not..\n:arrow_right:`{prefix}complain (pbid)` - Check the total number of complaints registered by that player.\n:arrow_right:`{prefix}complaints (pbid)` - Check the total number of complaints registered for that player.")
  
            elif m[0] == 'restart':
                await message.channel.send(f">>> ## __(To find out server code type {prefix}sc) __\n:arrow_right:**__SERVER QUIT COMMANDz:__**\n:arrow_right:`{prefix}quit` - To restart all servers in one click...!\n:arrow_right:`{prefix}(server-code)quit` - To restart a specific server :> ")
  
            elif m[0] == 'user':
                await message.channel.send(f">>> :arrow_right:**__WHITELIST COMMANDz:__**\n:arrow_right:`{prefix}useradd (dc user-ID)` - To add a user to the whilelist to use all bot commands.\n:arrow_right:`{prefix}userremove (dc user-ID)` - To remove a user from the whitelist.\n:arrow_right:`{prefix}form (role)` - Use this cmd to give a form to user if his eligible for admin or vip")
                
            # server have a pecific code to use cmd xD and this cmd made to know code of cmd
            elif m[0] == 'sc': 
                await message.channel.send(">>> :arrow_right:**{0} - {1}**".format(commands_prefix, servers))

            #check last messages xD
            elif m[0] == (cmd +'lm'):         
                try:
                    settings = setting.get_settings_data()
                    lm = settings["discordbot"]["lastmsg"]
                    limit = int(m[1]) if len(m) > 1 and m[1].isdigit() else 10  # Default limit is 10 if not provided or not a number
                    max_messages = 2000

                    if limit > max_messages:
                        await message.channel.send(":arrow_right:**`Limit exceeds maximum word count of 2000.`**")
                    else:       
                        # Define the file path within the tools directory
                        directory_path = os.path.join(_ba.env()["python_directory_user"], "tools")
                        file_path = os.path.join(directory_path, f"{lm}_messages.txt")

                        with open(file_path, "r") as file:
                            messages = file.readlines()

                        if messages:
                            # Get the last `limit` messages
                            last_messages = [msg for msg in messages if msg.startswith('pb-')][-limit:]

                            # Prepare the message to send
                            last_msg = [
                                f">>> :reminder_ribbon: **({len(messages)}) Last {limit} Messages Data of {servers}:**"
                            ]

                            for msg in last_messages:
                                last_msg.append(f":arrow_right:**{msg.strip()}**")

                            await message.channel.send("\n".join(last_msg))
                        else:
                            await message.channel.send(f":arrow_right:**`No One has messaged in {servers}.`**")
                except:
                    await message.channel.send(":arrow_right:**`Limit exceeds maximum word count of 2000.`**")

             #check player last messages xD
            elif m[0] == (cmd +'plm'):         
                try:
                    if len(m) == 3:
                        settings = setting.get_settings_data()
                        lm = settings["discordbot"]["lastmsg"]
                        pbids = m[1] 
                        limit = int(m[2]) if m[2].isdigit() else 10  # Default limit is 10 if not provided or not a number
                        max_messages = 2000

                        if limit > max_messages:
                            await message.channel.send("<a:arrow:1178624981593227265>**`Limit exceeds maximum word count of 2000.`**")
                        else:       
                            # Define the file path within the tools directory
                            directory_path = os.path.join(_ba.env()["python_directory_user"], "tools")
                            file_path = os.path.join(directory_path, f"{lm}_messages.txt")

                            with open(file_path, "r") as file:
                                messages = file.readlines()

                            if messages:
                                pbid_messages = [msg for msg in messages if msg.startswith(f'{pbids}')][-limit:]
                                if pbid_messages:
                                    last_msg = [
                                        f">>> <a:tag:1180192585277526077> **Player Last {limit} Messages Data of {servers}:**"
                                    ]
                                    for msg in pbid_messages:
                                        last_msg.append(f"<a:arrow:1178624981593227265>**{msg.strip()}**")

                                    total_length = sum(len(msg) for msg in last_msg)
                                    if total_length > max_messages:
                                        await send_message_chunks(message.channel, last_msg)
                                    else:
                                        await message.channel.send("\n".join(last_msg))
                                else:
                                    await message.channel.send(f"<a:arrow:1178624981593227265>**`No last messages found for the provided player ID in {servers}`**")
                            else:
                                await message.channel.send(f"<a:arrow:1178624981593227265>**`No One has messaged in {servers}.`**")
                    else:
                        await message.channel.send(">>> <a:arrow:1178627121137074226>**<a:wrong:1178796743681392681>Invalid Format! Use `{0}{1}plm <pbid> <limit>`**".format(prefix, commands_prefix))
                except:
                    await message.channel.send("<a:arrow:1178624981593227265>**`Limit exceeds maximum word count of 2000.`**")

            # quit in single server :)
            elif m[0] == (cmd +'quit'):
                await message.channel.send(">>> :arrow_right:**<a:correct:1178796582334898326>`Successfully restarted {0}` **".format(servers))         
                ba.quit()

           # add coins to player in a specific server
            elif m[0] == (cmd +'addcoins'):
                if len(m) == 3:
                    ac = m[1]
                    count = int(m[2])                    
                    coin = nc.getcoins(ac)                    
                    if coin:
                        addcoins(ac, count)    
                        await message.channel.send(f">>> :arrow_right:**Successfully added {count} coins to PB ID `{ac}` in {servers}**")                    
                    else:
                        await message.channel.send(f">>> :arrow_right:**User `{ac}` is not there in my bankdata in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}addcoins <pbid> <count>`**".format(prefix, commands_prefix))

          # remove coins to player in a specific server
            elif m[0] == (cmd +'removecoins'):
                if len(m) == 3:
                    ac = m[1]
                    count = int(m[2])                    
                    coin = nc.getcoins(ac)                    
                    if coin:
                        removecoins(ac, count)    
                        await message.channel.send(f">>> :arrow_right:**Successfully Removed {count} coins from PB ID `{ac}` in {servers}**")                    
                    else:
                        await message.channel.send(f">>> :arrow_right:**User `{ac}` is not there in my bankdata in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}removecoins <pbid> <count>`**".format(prefix, commands_prefix))

           # add coins to player in all servers
            elif m[0] == 'addcoins':
                if len(m) == 3:
                    ac = m[1]
                    count = int(m[2])                    
                    coin = nc.getcoins(ac)                    
                    if coin:
                        addcoins(ac, count)    
                        await message.channel.send(f">>> :arrow_right:**Successfully added {count} coins to PB ID `{ac}` in {servers}**")                    
                    else:
                        await message.channel.send(f">>> :arrow_right:**User `{ac}` is not there in my bankdata in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}addcoins <pbid> <count>`**".format(prefix))

          # remove coins to player in all servers
            elif m[0] == 'removecoins':
                if len(m) == 3:
                    ac = m[1]
                    count = int(m[2])                    
                    coin = nc.getcoins(ac)                    
                    if coin:
                        removecoins(ac, count)    
                        await message.channel.send(f">>> :arrow_right:**Successfully Removed {count} coins from PB ID `{ac}` in {servers}**")                    
                    else:
                        await message.channel.send(f">>> :arrow_right:**User `{ac}` is not there in my bankdata in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}removecoins <pbid> <count>`**".format(prefix))

            # add server stats data in specific server 
            elif m[0] == (cmd +'csd'):
                if len(m) == 4:   
                     stats = mystats.get_all_stats()    
                     pbid = m[1]   
                     reply = m[2]
                     space = ""
                     statsdata = space+reply+space
                     data = int(m[3])

                     if pbid in stats:
                         stats[pbid][statsdata] = data 
                         mystats.dump_stats(stats)
                         mystats.refreshStats()
                         await message.channel.send(f">>> :arrow_right:**`{m[1]}` `{reply}` changed to `{data} {reply}` in {servers}**")
                     else:
                         await message.channel.send(f">>> :arrow_right:**User `{m[1]}` statsdata is not available in {servers}**")
                                           
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}csd <pbid> <data to change> <count>`**".format(prefix, commands_prefix))

            #to check who joined recently in specific server xD
            elif m[0] == (cmd +'recents'):
                limit = 10 

                if len(m) >= 2:
                   
                    try:
                        limit = int(m[1])
                    except ValueError:
                       
                        pass

                if serverdata.recents:
                    await message.channel.send(f">>> :reminder_ribbon:**Recently Joined Players Data of {servers}:**")
                    for i, players in enumerate(serverdata.recents[:limit]):
                        await message.channel.send(f">>> :arrow_right:**Name: {players['deviceId']}, PlayerID: {players['pbid']}, ClientID: {players['client_id']} **") 
                        if i == limit - 1: 
                            break
                else:
                    await message.channel.send(f">>> :arrow_right:**No one played currently in {servers} **")

            #maxplayer set from dc in specific server. :))))
            elif m[0] == (cmd +'mp'):
                if len(m) == 2:                      
                    mp = int(m[1])
                    sp = m[1]
                    if mp:
                        ba.internal.set_public_party_max_size(mp)
                        await message.channel.send(f">>> :arrow_right:**Maximum players set to {mp} in {servers}**")     
                    else:    
                        await message.channel.send(f">>> :arrow_right:**Error!!: Enter number**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}mp <count>`**".format(prefix, commands_prefix))

            # cmd list of any role in a specific server :)
            elif m[0] == (cmd +'cmdlist'):
                a = message.content.lower().split()
                b = message.content.upper().split()
                if len(a) == 2 or len(b) == 2:
                     roles = pdata.get_roles()
                     rol = b[1]
                     role = a[1]
                     if role in roles:         
                         role_data = [
                             f">>> :arrow_right:**__{rol}'S COMMANDS LIST OF {servers}:__**"
                         ]               
 
                         data = pdata.roles_cmdlist(role)
                         role_data.append(f"{data}")
                         await message.channel.send("\n".join(role_data))                        
                     else:              
                         await message.channel.send(f">>> :arrow_right:**Use Roles: `Owner, Moderator, Staff, Admin, Vip`**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}cmdlist <role>`**".format(prefix, commands_prefix))

            # to kick player from server by Discord Cmd xD
            elif m[0] == (cmd +'kick'):
                if len(m) == 2:
                    pbid = m[1]
                    if serverdata.recents:
                        pdata.dckick(pbid)
                        await message.channel.send(f">>> :arrow_right:**kicked `{pbid}` from {servers}**")                
                    else:
                        await message.channel.send(f">>> :arrow_right:**`{pbid}` not joined the server yet..!**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}kick <pbid>`**".format(prefix, commands_prefix))



            # ban in all server xD                   
            elif m[0] == 'bsban':
                m = message.content[2:].split()
                if m[0] == 'bsban':
                    if len(m) == 4:
                        banned = mongo.Banlist.find_one() or {'ban': {'ids': [], 'deviceids': [],'ips': []}}
                        pb_id, device_id, ip_address= m[1], m[2],m[3]
                        if pb_id in banned['ban']['ids'] and device_id in banned['ban']['deviceids'] and ip_address in banned['ban']['ips']:
                            await message.channel.send(f">>> :arrow_right:**User is already banned in {servers}** ")
                        else:
                            banned['ban']['ids'].append(m[1])                            
                            banned['ban']['deviceids'].append(m[2])
                            banned['ban']['ips'].append(m[3])
                            mongo.Banlist.delete_many({})
                            mongo.Banlist.insert_one(banned)
                            # print("After banning:")
                            # print("IDs:", banned['ban']['ids'])
                            # print("IPs:", banned['ban']['ips'])
                            # print("Device IDs:", banned['ban']['deviceids'])
                            await message.channel.send(f">>> :arrow_right:**Successfully banned `{m[1]}` in all servers **")
                            pdata.mongokick(pb_id)
                    else:
                        await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}bsban <pbid> <deviceid> <ip or name>`!!**".format(prefix))

            #check banned player in all servers :)))
            elif m[0] == 'bancheck':
                banned = mongo.Banlist.find_one() or {'ban': {'ids': [], 'deviceids': [], 'ips': []}}
                if banned and 'ban' in banned:
                    banned_ids = banned['ban']['ids']
                    banned_device_ids = banned['ban']['deviceids']
                    banned_ips = banned['ban']['ips']

                    if len(m) == 2: 
                        pb_id_to_check = m[1]
                        if pb_id_to_check in banned_ids:
                            index = banned_ids.index(pb_id_to_check)
                            device_id = banned_device_ids[index]
                            ip = banned_ips[index]
                            await message.channel.send(f">>> :arrow_right:**`Player with PB-ID {pb_id_to_check} is Banned in all servers.Device-ID: {device_id}, IP: {ip}`  **")
                        else:
                            await message.channel.send(">>> :arrow_right:**`Player with PB-ID : {0} is not banned in all servers.`**".format(pb_id_to_check))
                    else:
                        await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}bancheck <pbid>`**".format(prefix))

            # check banned player in specific server 
            elif m[0] == (cmd +'bancheck'):
                blacklist_data = pdata.get_blacklist()

                if blacklist_data and 'ban' in blacklist_data:
                    banned_ids = blacklist_data['ban']['ids']
                    banned_device_ids = blacklist_data['ban']['deviceids']
                    banned_ips = blacklist_data['ban']['ips']

                    if len(m) == 2: 
                        pb_id_to_check = m[1]
                        if pb_id_to_check in banned_ids:
                            await message.channel.send(f">>> :arrow_right:**`Player with PB-ID {pb_id_to_check} is Banned in {servers}!`  **")
                        else:
                            await message.channel.send(">>> :arrow_right:**`Player with PB-ID : {0} is not banned in {1}.`**".format(pb_id_to_check, servers))
                    else:
                        await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}bancheck <pbid>`**".format(prefix, commands_prefix))

            #check last 10 banned players :D
            elif m[0] == (cmd+'mbanlist'):
                    banned = mongo.Banlist.find_one() or {'ban': {'ids': [], 'deviceids': [], 'ips': []}}
                    if banned and 'ban' in banned:
                        banned_ids = banned['ban']['ids']
                        banned_device_ids = banned['ban']['deviceids']
                        banned_ips = banned['ban']['ips']

                        if banned_ids:
                            ban_messages = [
                                f">>> <:Cross:1178624823656714280> **Last 10 Banned Players in mongodb ({len(banned_ids)}):**"
                            ]

                            start_index = max(0, len(banned_ids) - 10)
                            for i in range(start_index, len(banned_ids)):
                                pb_id = banned_ids[i]
                                device_id = banned_device_ids[i]
                                ip = banned_ips[i]
                                ban_messages.append(f":arrow_right:**`PB-ID: {pb_id}, Device-ID: {device_id}, Ip: {ip}` **")

                            await message.channel.send("\n".join(ban_messages))
                        else:
                            await message.channel.send(":arrow_right:**`No players are currently banned.`**")
                    else:
                        await message.channel.send(":arrow_right:**No ban data found.**")

            #check the admin list and count             
            elif m[0] == (cmd +'adminlist'):
                roles = pdata.get_roles()    
                stats = mystats.get_all_stats()                 
                if roles and 'admin' in roles:
                    admin_ids = roles['admin']['ids']
                    if admin_ids:             
                        await message.channel.send(f">>> :reminder_ribbon:**Admins_Count ({len(admin_ids)}):**")
                        for i in range(len(admin_ids)):
                            pb_id = admin_ids[i]  
                            await message.channel.send(f">>> :arrow_right:**PB-ID: `{pb_id}`**")
                            name = stats[pb_id]['name']
                            score = stats[pb_id]['scores']     
                            rank = stats[pb_id]['rank']     
                            await message.channel.send(f">>> :arrow_right:**[ Name: `{name}`, Rank: `{rank}`, Scores: `{score}` ]**")
                    else:
                        await message.channel.send(">>> :arrow_right:**`No one is admin currently in {0}.`**".format(servers))
                else:
                    await message.channel.send(">>> :arrow_right:**No admin data found.**")            

            #vip count cmd 
            elif m[0] == (cmd +'viplist'):
                roles = pdata.get_roles()
                stats = mystats.get_all_stats()  
                if roles and 'vip' in roles:
                    vip_ids = roles['vip']['ids']
                    if vip_ids:          
                        await message.channel.send(f">>> :reminder_ribbon:**Vips_Count ({len(vip_ids)}):**")
                        for i in range(len(vip_ids)):
                            pb_id = vip_ids[i]   
                            await message.channel.send(f">>> :arrow_right:**PB-ID: `{pb_id}`**")
                            name = stats[pb_id]['name']
                            score = stats[pb_id]['scores']     
                            rank = stats[pb_id]['rank']                                 
                            await message.channel.send(f">>> :arrow_right:**[ Name: `{name}`, Rank: `{rank}`, Scores: `{score}` ]**")
                    else:
                        await message.channel.send(">>> :arrow_right:**`No one is vip currently in {0}.`**".format(servers))
                else:
                    await message.channel.send(">>> :arrow_right:**No vip data found.**")            

            #cs count cmd 
            elif m[0] == (cmd +'cslist'):
                roles = pdata.get_roles()
                if roles and 'staff' in roles:
                    cs_ids = roles['staff']['ids']
                    if cs_ids:          
                        await message.channel.send(f">>> :reminder_ribbon:**CS_Count ({len(cs_ids)}):**")
                        for i in range(len(cs_ids)):
                            pb_id = cs_ids[i]
                            await message.channel.send(f">>> :arrow_right:**PB-ID: `{pb_id}`**")
                    else:
                        await message.channel.send(">>> :arrow_right:**`No one is cs currently in {0}.`**".format(servers))
                else:
                    await message.channel.send(">>> :arrow_right:**No cs data found.**")            

            #mod count cmd 
            elif m[0] == (cmd +'modlist'):
                roles = pdata.get_roles()
                if roles and 'moderator' in roles:
                    mod_ids = roles['moderator']['ids']
                    if mod_ids:          
                        await message.channel.send(f">>> :reminder_ribbon:**Mods_Count ({len(mod_ids)}):**")
                        for i in range(len(mod_ids)):
                            pb_id = mod_ids[i]
                            await message.channel.send(f">>> :arrow_right:**PB-ID: `{pb_id}`**")
                    else:
                        await message.channel.send(">>> :arrow_right:**`No one is mod currently in {0}.`**".format(servers))
                else:
                    await message.channel.send(">>> :arrow_right:**No mod data found.**")            

            #leadstaff count cmd 
            elif m[0] == (cmd +'leadstafflist'):
                roles = pdata.get_roles()
                if roles and 'leadstaff' in roles:
                    leadstaff_ids = roles['leadstaff']['ids']
                    if leadstaff_ids:          
                        await message.channel.send(f">>> :reminder_ribbon:**Leadstaffs_Count ({len(leadstaff_ids)}):**")
                        for i in range(len(leadstaff_ids)):
                            pb_id = leadstaff_ids[i]
                            await message.channel.send(f">>> :arrow_right:**PB-ID: `{pb_id}`**")
                    else:
                        await message.channel.send(f">>> :arrow_right:**`No one is leadstaff currently in {servers}.`**")
                else:
                    await message.channel.send(">>> :arrow_right:**No leadstaff data found.**")            

            #roles count cmd :))))))
            elif m[0] == (cmd +'roleslist'):
                      custom_data = pdata.get_roles()
                      reply = ""
                      tag_data = custom_data
                      if tag_data:
                          tag_count = len(tag_data)
                          await message.channel.send(f">>> :reminder_ribbon:**`({tag_count})` Roles in {servers}:**")  
                          for role in tag_data:        
                                reply = reply+role+", "                                                
                          await message.channel.send(f">>> :arrow_right:**{reply}**")                                               
                      else:
                          await message.channel.send(f">>> :arrow_right:**`No roles currently in {servers}.`**")
                    
            #owner count cmd 
            elif m[0] == (cmd +'ownerlist'):
                roles = pdata.get_roles()
                if roles and 'owner' in roles:
                    owner_ids = roles['owner']['ids']
                    if owner_ids:          
                        await message.channel.send(f">>> :reminder_ribbon:**Owners_Count ({len(owner_ids)}):**")
                        for i in range(len(owner_ids)):
                            pb_id = owner_ids[i]
                            await message.channel.send(f">>> :arrow_right:**PB-ID: `{pb_id}`**")
                    else:
                        await message.channel.send(">>> :arrow_right:**`No one is owner currently in {0}.`**".format(servers))
                else:
                    await message.channel.send(">>> :arrow_right:**No owner data found.**")            
                    
            #tag count cmd :))))))
            elif m[0] == (cmd +'taglist'):
                custom_data = pdata.get_custom()
                if custom_data and 'customtag' in custom_data:
                    tag_data = custom_data['customtag']
                    if tag_data:
                        tag_count = len(tag_data)
                        tag_list = "\n".join([f":arrow_right:PB-ID: `{pb_id}`\n:arrow_right:CUSTOM-TAG: `{tag}`" for pb_id, tag in tag_data.items()])
                        await message.channel.send(f">>> :reminder_ribbon:**`({tag_count})` Custom tags in {servers}:\n{tag_list}**")
                    else:
                        await message.channel.send(">>> :arrow_right:**`No one got tag currently in {0}.`**".format(servers))
                else:
                    await message.channel.send(">>> :arrow_right:**No tag data found.**")            


            #effect count cmd :))))))
            elif m[0] == (cmd +'effectlist'):
                custom_data = pdata.get_custom()
                if custom_data and 'customeffects' in custom_data:
                    effect_data = custom_data['customeffects']
                    if effect_data:
                        effect_count = len(effect_data)
                        effect_list = "\n".join([f":arrow_right:PB-ID: `{pb_id}`\n:arrow_right:CUSTOM-EFFECT: `{effect}`" for pb_id, effect in effect_data.items()])
                        await message.channel.send(f">>> <a:emoji_81:1089458873825497138>**`({effect_count})` Custom Effects in {servers}:\n{effect_list}**")
                    else:
                        await message.channel.send(">>> :arrow_right:**`No one got effect currently in {0}.`**".format(servers))
                else:
                    await message.channel.send(">>> :arrow_right:**No effect data found.**")            

            #mute count cmd :))))))
            elif m[0] == (cmd +'mutelist'):
                black_data = pdata.get_blacklist()
                if black_data and 'muted-ids' in black_data:
                    mute_data = black_data['muted-ids']
                    if mute_data:
                        mute_count = len(mute_data)
                        mute_list = "\n".join([f":arrow_right:PB-ID: `{pb_id}` " for pb_id, data in mute_data.items()])
                        await message.channel.send(f">>> :reminder_ribbon:**`({mute_count})` Muted player in {servers}:\n{mute_list}**")
                    else:
                        await message.channel.send(">>> :arrow_right:**`No one is muted currently in {0}.`**".format(servers))
                else:
                    await message.channel.send(">>> :arrow_right:**No mute data found.**")            

            #disable kick vote list and count :))
            elif m[0] == (cmd +'dkickvotelist'):
                black_data = pdata.get_blacklist()
                if black_data and 'kick-vote-disabled' in black_data:
                    kickvote_data = black_data['kick-vote-disabled']
                    if kickvote_data:
                        kickvote_count = len(kickvote_data)
                        kickvote_list = "\n".join([f":arrow_right:PB-ID: `{pb_id}` " for pb_id, data in kickvote_data.items()])
                        await message.channel.send(f">>> :reminder_ribbon:**`({kickvote_count})` Disable server kick-vote player in {servers}:\n{kickvote_list}**")
                    else:
                        await message.channel.send(">>> :arrow_right:**`No one is disabled server kick-vote currently in {0}.`**".format(servers))
                else:
                    await message.channel.send(">>> :arrow_right:**No disable server kick-vote data found.**")            
                    
            #ban count of any server :>
            elif m[0] == (cmd +'banlist'):
                black_data = pdata.get_blacklist()
                if black_data and 'ban' in black_data:
                    ban_data = black_data['ban']['ids']
                    if ban_data:
                        ban_count = len(ban_data)
                        last_10_keys = list(ban_data.keys())[-10:]  # Retrieve the last 10 keys
                        last_10_bans = {pb_id: ban_data[pb_id] for pb_id in last_10_keys}  # Retrieve the corresponding data
                        ban_list = "\n".join([f":arrow_right:PB-ID: `{pb_id}` " for pb_id in last_10_bans])
                        await message.channel.send(f">>> <:Cross:1192229645177851994>**`({ban_count})` Last 10 Banned player in {servers}:**")
                        await message.channel.send(f">>> **{ban_list}**")
                    else:
                        await message.channel.send(">>> :arrow_right:**`No one is banned currently in {0}.`**".format(servers))
                else:
                    await message.channel.send(">>> :arrow_right:**No banned data found.**")            

            #single server ban, which will ban in server files
            elif m[0] == (cmd +'ban'):
                if len(m) == 4: 
                    banned = pdata.get_blacklist()
                    pb_id, time, reason= m[1], int(m[2]),m[3]
                    if pb_id in banned['ban']['ids']:
                        await message.channel.send(f">>> :arrow_right:**User is already banned in {servers}** ")
                    else:
                        pdata.ban_player(pb_id, time, reason)    
                        pdata.update_blacklist()                 
                        await message.channel.send(f">>> :arrow_right:**Successfully banned `{m[1]}` in {servers} **")
                        pdata.mongokick(pb_id)
                else:
                    await message.channel.send(">>> :arrow_right::x:**Invalid Format! Use `{0}{1}ban <pbid> <time in days> <reason no space>`**".format(prefix, commands_prefix))

            # unban in single server
            elif m[0] == (cmd +'unban'):
                if len(m) == 2:
                    banned = pdata.get_blacklist()
                    pb_id = m[1]
                    if pb_id in banned['ban']['ids']:
                        pdata.unban_player(pb_id)   
                        pdata.update_blacklist()                  
                        await message.channel.send(f">>> :arrow_right:**Successfully unbanned `{m[1]}` in {servers} **")
                    else:
                        await message.channel.send(f">>> :arrow_right:**User `{m[1]}` is not banned in {servers}!**")                       
                else:
                    await message.channel.send(">>> :arrow_right::x:**Invalid Format! Use `{0}{1}unban <pbid>`**".format(prefix, commands_prefix))

            #single server disable kick vote :)
            elif m[0] == (cmd +'dkickvote'):
                if len(m) == 4: 
                    kickvote = pdata.get_blacklist()
                    pb_id, time, reason= m[1], int(m[2]),m[3]
                    if pb_id in kickvote['kick-vote-disabled']:
                        await message.channel.send(f">>> :arrow_right:**User server kick-vote is already disabled in {servers}** ")
                    else:
                        pdata.disable_kick_vote(pb_id, time, reason)   
                        pdata.update_blacklist()                  
                        await message.channel.send(f">>> :arrow_right:**Successfully disable server kick-vote to `{m[1]}` in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right::x:**Invalid Format! Use `{0}{1}dkickvote <pbid> <time in days> <reason no space>`**".format(prefix, commands_prefix))

            # enable kick-vote in single server
            elif m[0] == (cmd +'ekickvote'):
                if len(m) == 2:
                    kickvote = pdata.get_blacklist()
                    pb_id = m[1]
                    if pb_id in kickvote['kick-vote-disabled']:
                        pdata.enable_kick_vote(pb_id)  
                        pdata.update_blacklist()                   
                        await message.channel.send(f">>> :arrow_right:**Successfully enable server kick-vote to `{m[1]}` in {servers} **")
                    else:
                        await message.channel.send(f">>> :arrow_right:**User `{m[1]}` is not disabled server kick-vote in {servers}!**")                       
                else:
                    await message.channel.send(">>> :arrow_right::x:**Invalid Format! Use `{0}{1}ekickvote <pbid>`**".format(prefix, commands_prefix))

            #all server disable server kick-vote :))))))
            elif m[0] == 'dkickvote':
                if len(m) == 4: #
                    kickvote = pdata.get_blacklist()
                    pb_id, time, reason= m[1], int(m[2]),m[3]
                    if pb_id in kickvote['kick-vote-disabled']:
                        await message.channel.send(f">>> :arrow_right:**User server kick-vote is already disabled in {servers}** ")
                    else:
                        pdata.disable_kick_vote(pb_id, time, reason)
                        pdata.update_blacklist()                     
                        await message.channel.send(f">>> :arrow_right:**Successfully disable server kick-vote to `{m[1]}` in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right::x:**Invalid Format! Use `{0}dkickvote <pbid> <time in days> <reason no space>`**".format(prefix))

            # enable kick-vote in all server
            elif m[0] == 'ekickvote':
                if len(m) == 2:
                    kickvote = pdata.get_blacklist()
                    pb_id = m[1]
                    if pb_id in kickvote['kick-vote-disabled']:
                        pdata.enable_kick_vote(pb_id)   
                        pdata.update_blacklist()                  
                        await message.channel.send(f">>> :arrow_right:**Successfully enable server kick-vote to `{m[1]}` in {servers} **")
                    else:
                        await message.channel.send(f">>> :arrow_right:**User `{m[1]}` is not disabled server kick-vote in {servers}!**")                       
                else:
                    await message.channel.send(">>> :arrow_right::x:**Invalid Format! Use `{0}ekickvote <pbid>`**".format(prefix))
                                                                                                   
         #normal mute system for single server
         #but if u will connect one bot to all servers it gonna mute in all servers. 
            elif m[0] == 'bsmute':
                if len(m) >= 2:
                        print(f"Length of m: {len(m)}")
                        if len(m) >= 3:
                            try:
                                duration = datetime.timedelta(minutes=int(m[2]))
                            except ValueError:
                                    await message.channel.send(">>> :arrow_right:**:x:Invalid time format. Please use minutes as a numeric value.**")
                                    return
                        else:
                            duration = datetime.timedelta(days=1000)  # Default: 1000 day hahaha
                        # base_path = os.path.join(_ba.env()['python_directory_user'], "playersData" + os.sep)
                        # rolesfile = os.path.join(base_path, 'blacklist.json')
                        blacklist = pdata.get_blacklist()                        
                        # Check if the user is already muted
                        if m[1] in blacklist.get('muted-ids', {}):
                            await message.channel.send(f">>> :arrow_right:**User is already muted! in {servers}** ")

                        else:
                            # Calculate the expiration time
                            expiration_time = (datetime.datetime.now() + duration).strftime("%Y-%m-%d %H:%M:%S")
                            # Add the user to the muted-ids section
                            blacklist['muted-ids'][m[1]] = {
                                "till": expiration_time,
                                "reason": m[3]
                            }
                            await message.channel.send(f">>> :arrow_right:**Successfully muted `{m[1]}` in {servers}  **")
                            pdata.update_blacklist()
                            # Save updated blacklist to JSON file
                            # with open(rolesfile, 'w') as file:
                            #     json.dump(blacklist, file, indent=4)
                                #await message.channel.send(f"**Successfully muted `{m[1]}` for {m[2]} minutes!**")

                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}bsmute <pbid> <time in minutes> <reason no space>`**".format(prefix))

            # unmute in all server xD
            elif m[0] == 'bsunmute':
                if len(m) == 2:
                    # base_path = os.path.join(_ba.env()['python_directory_user'], "playersData" + os.sep)
                    # rolesfile = os.path.join(base_path, 'blacklist.json')
                    blacklist = pdata.get_blacklist()                  
                   
                    if m[1] in blacklist.get('muted-ids', {}):
                       
                        del blacklist['muted-ids'][m[1]]
                        pdata.update_blacklist()
                       
                        # with open(rolesfile, 'w') as file:
                        #     json.dump(blacklist, file, indent=4)

                        await message.channel.send(f">>> :arrow_right:**Successfully unmuted `{m[1]}` in {servers}  **")
                    else:
                        await message.channel.send(f">>> :arrow_right:**User `{m[1]}` is not muted in {servers}  **")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}bsunmute <pbid>`**".format(prefix))

            #mute in anyone server :)!
            elif m[0] == (cmd +'mute'):
                if len(m) >= 2:
                        print(f"Length of m: {len(m)}")
                        if len(m) >= 3:
                            try:
                                duration = datetime.timedelta(minutes=int(m[2]))
                            except ValueError:
                                    await message.channel.send(">>> :arrow_right:**:x:Invalid time format. Please use minutes as a numeric value.**")
                                    return
                        else:
                            duration = datetime.timedelta(days=1000)  # Default: 1000 day hahaha
                        #base_path = os.path.join(_ba.env()['python_directory_user'], "playersData" + os.sep)
                        #rolesfile = os.path.join(base_path, 'blacklist.json')
                        blacklist = pdata.get_blacklist()                        
                       
                        if m[1] in blacklist.get('muted-ids', {}):
                            await message.channel.send(f">>> :arrow_right:**User is already muted! in {servers}** ")

                        else:
                         
                            expiration_time = (datetime.datetime.now() + duration).strftime("%Y-%m-%d %H:%M:%S")
                           
                            blacklist['muted-ids'][m[1]] = {
                                "till": expiration_time,
                                "reason": m[3]
                            }
                            await message.channel.send(f">>> :arrow_right:**Successfully muted `{m[1]}` in {servers}  **")
                            pdata.update_blacklist()
                          
                            #with open(rolesfile, 'w') as file:
                               # json.dump(blacklist, file, indent=4)
                                #await message.channel.send(f"**Successfully muted `{m[1]}` for {m[2]} minutes!**")

                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}mute <pbid> <time in minutes> <reason no space>`**".format(prefix, commands_prefix))
                    
           #unmute player in anyone server :)
            elif m[0] == (cmd +'unmute'):
                if len(m) == 2:
                    #base_path = os.path.join(_ba.env()['python_directory_user'], "playersData" + os.sep)
                    #rolesfile = os.path.join(base_path, 'blacklist.json')
                    blacklist = pdata.get_blacklist()                  
                   
                    if m[1] in blacklist.get('muted-ids', {}):
                        
                        del blacklist['muted-ids'][m[1]]
                        pdata.update_blacklist()
                       
                        #with open(rolesfile, 'w') as file:
                            #json.dump(blacklist, file, indent=4)

                        await message.channel.send(f">>> :arrow_right:**Successfully unmuted `{m[1]}` in {servers}  **")
                    else:
                        await message.channel.send(f">>> :arrow_right:**User `{m[1]}` is not muted in {servers}  **")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}unmute <pbid>`**".format(prefix, commands_prefix))
                    

            elif m[0] == (cmd +'cr'):
                if len(m) == 3:
                      roles = pdata.get_roles()
                      role = m[1].lower()
                      rtag = m[2]
                      if role in roles:
                          await message.channel.send(f">>> :arrow_right:**`{m[1]}` role already exists in {servers} **")
                      else:
                          roles[role] = {
                              "tag": rtag,
                              "tagcolor": [1, 1, 1],
                              "commands": [],
                              "ids": [],
                          }
                          await message.channel.send(f">>> :arrow_right:**Successfully Created [ `{m[1].upper()}` ROLE ] in {servers} **")
                          pdata.updates_roles()

                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}cr <role> <tag>`**".format(prefix, commands_prefix))

       
            elif m[0] == (cmd +'rr'):
                if len(m) == 2:
                      roles = pdata.get_roles()
                      role = m[1].lower()
                      if role in roles:
                          del roles[role]
                          await message.channel.send(f">>> :arrow_right:**Successfully Removed [ `{m[1].upper()}` ROLE ] from {servers} **")
                          pdata.updates_roles()
                      else:
                          await message.channel.send(f">>> :arrow_right:**`{m[1]}` role doesn't exists in {servers} **")

                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}rr <role>`**".format(prefix, commands_prefix))
       
            elif m[0] == (cmd +'crtag'):
                if len(m) == 3:      
                      roles = pdata.get_roles()                                      
                      role = m[1].lower()
                      tag = m[2]
                      if role in roles:
                          pdata.change_role_tag(role,tag)
                          await message.channel.send(f">>> :arrow_right:**Successfully Changed [ `{m[1].upper()}` ] role tag to [ `{tag}` ] in {servers} **")
                      else:
                          await message.channel.send(f">>> :arrow_right:**`{m[1]}` role doesn't exists in {servers} **")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}crtag <role> <tag>`**".format(prefix, commands_prefix))

            elif m[0] == 'cr':
                if len(m) == 3:
                      roles = pdata.get_roles()
                      role = m[1].lower()
                      rtag = m[2]
                      if role in roles:
                          await message.channel.send(f">>> :arrow_right:**`{m[1]}` role already exists in {servers} **")
                      else:
                          roles[role] = {
                              "tag": rtag,
                              "tagcolor": [1, 1, 1],
                              "commands": [],
                              "ids": [],
                          }
                          await message.channel.send(f">>> :arrow_right:**Successfully Created [ `{m[1].upper()}` ROLE ] in {servers} **")
                          pdata.updates_roles()

                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}cr <role> <tag>`**".format(prefix))

       
            elif m[0] == 'rr':
                if len(m) == 2:
                      roles = pdata.get_roles()
                      role = m[1].lower()
                      if role in roles:
                          del roles[role]
                          await message.channel.send(f">>> :arrow_right:**Successfully Removed [ `{m[1].upper()}` ROLE ] from {servers} **")
                          pdata.updates_roles()
                      else:
                          await message.channel.send(f">>> :arrow_right:**`{m[1]}` role doesn't exists in {servers} **")

                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}rr <role>`**".format(prefix))
       
            elif m[0] == 'crtag':
                if len(m) == 3:      
                      roles = pdata.get_roles()                                      
                      role = m[1].lower()
                      tag = m[2]
                      if role in roles:
                          pdata.change_role_tag(role,tag)
                          await message.channel.send(f">>> :arrow_right:**Successfully Changed [ `{m[1].upper()}` ] role tag to [ `{tag}` ] in {servers} **")
                      else:
                          await message.channel.send(f">>> :arrow_right:**`{m[1]}` role doesn't exists in {servers} **")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}crtag <role> <tag>`**".format(prefix))
  
### ADD ROLE SECTION

            elif m[0] == 'addrole':
                if len(m) >= 3:
                    role_name = m[1].lower()  
                    pb_id = m[2]
                    reply = ""
                    roles_data = pdata.get_roles()        
                    if role_name not in roles_data:
                        for role in roles_data:        
                            reply = reply+role+", "                  
                        await channel.send(f">>> :arrow_right:**`Use Role - {reply}`**")
        
                    if pb_id in roles_data.get(role_name, {}).get('ids', []):
                        await channel.send(f">>> :arrow_right:**User is already in the [ {role_name.upper()} ] role in {servers}**")
                    else:
                        roles_data[role_name]['ids'].append(pb_id)
                        if role_name == 'owner':
                           await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name in ['leadstaff', 'lead-staff']:
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name == 'moderator':
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name in ['cs', 'staff']:
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name == 'tcs':
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name == 'admin':
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name == 'vip':
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        else:
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        pdata.updates_roles()
                else:
                    await channel.send(f">>> :arrow_right:**:x:Invalid Format! Use `{prefix}addrole <role> <pbid>`**")

            elif m[0] == 'removerole':
                if len(m) >= 3:
                    role_name = m[1].lower()  
                    pb_id = m[2]
                    reply = ""
                    roles_data = pdata.get_roles()        
                    if role_name not in roles_data:
                        for role in roles_data:        
                            reply = reply+role+", "                  
                        await channel.send(f">>> :arrow_right:**`Use Role - {reply}`**")
                    else:
                        if pb_id in roles_data.get(role_name, {}).get('ids', []):
                            roles_data[role_name]['ids'].remove(pb_id)                            
                            if role_name == 'owner':
                               await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['leadstaff', 'lead-staff']:
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'moderator':
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['cs', 'staff']:
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'tcs':
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'admin':
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'vip':
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            else:
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            pdata.updates_roles()                               
                        else:
                            if role_name == 'owner':
                               await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['leadstaff', 'lead-staff']:
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'moderator':
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['cs', 'staff']:
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'tcs':
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'admin':
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'vip':
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            else:
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            
                else:
                    await channel.send(f">>> :arrow_right:**:x:Invalid Format! Use `{prefix}removerole <role> <pbid>`**")
#########
            #cmd to add any role
            elif m[0] == (cmd + 'addrole'):
                if len(m) >= 3:
                    role_name = m[1].lower()  
                    pb_id = m[2]
                    reply = ""
                    roles_data = pdata.get_roles()        
                    if role_name not in roles_data:
                        for role in roles_data:        
                            reply = reply+role+", "                  
                        await channel.send(f">>> :arrow_right:**`Use Role - {reply}`**")
        
                    if pb_id in roles_data.get(role_name, {}).get('ids', []):
                        await channel.send(f">>> :arrow_right:**User is already in the [ {role_name.upper()} ] role in {servers}**")
                    else:
                        roles_data[role_name]['ids'].append(pb_id)
                        if role_name == 'owner':
                           await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name in ['leadstaff', 'lead-staff']:
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name == 'moderator':
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name in ['cs', 'staff']:
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name == 'tcs':
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name == 'admin':
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        elif role_name == 'vip':
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        else:
                            await channel.send(f">>> :arrow_right:**Successfully added `{pb_id}` as an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                        pdata.updates_roles()
                else:
                    await channel.send(f">>> :arrow_right:**:x:Invalid Format! Use `{prefix}{commands_prefix}addrole <pbid> <role>`**")

            elif m[0] == (cmd + 'removerole'):
                if len(m) >= 3:
                    role_name = m[1].lower()  
                    pb_id = m[2]
                    reply = ""
                    roles_data = pdata.get_roles()        
                    if role_name not in roles_data:
                        for role in roles_data:        
                            reply = reply+role+", "                  
                        await channel.send(f">>> :arrow_right:**`Use Role - {reply}`**")
                    else:            
                        if pb_id in roles_data.get(role_name, {}).get('ids', []):
                            roles_data[role_name]['ids'].remove(pb_id)
                            if role_name == 'owner':
                               await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['leadstaff', 'lead-staff']:
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'moderator':
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['cs', 'staff']:
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'tcs':
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'admin':
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'vip':
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            else:
                                await channel.send(f">>> :arrow_right:**Successfully removed `{pb_id}` from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            pdata.updates_roles()                               
                        else:
                            if role_name == 'owner':
                               await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['leadstaff', 'lead-staff']:
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'moderator':
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['cs', 'staff']:
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'tcs':
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'admin':
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'vip':
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            else:
                                await channel.send(f">>> :arrow_right:**User `{pb_id}` is not an [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            
                else:
                    await channel.send(f">>> :arrow_right:**:x:Invalid Format! Use `{prefix}{commands_prefix}removerole <pbid> <role>`**")

#REMOVE ROLES IDS AND CUSTOMS IDS SECTION 

            elif m[0] == (cmd +'rids'):
                if len(m) >= 2:
                    role_name = m[1].lower()  
                    reply = ""
                    roles_data = pdata.get_roles()        
                    if role_name not in roles_data:
                        for role in roles_data:        
                            reply = reply+role+", "                  
                        await channel.send(f">>> :arrow_right:**`Use Role - {reply}`**")
                    else:
                        if roles_data[role_name]['ids']:
                            roles_data[role_name]['ids'] = []                      
                            if role_name == 'owner':
                               await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['leadstaff', 'lead-staff']:
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'moderator':
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['cs', 'staff']:
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'tcs':
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'admin':
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'vip':
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            else:
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            pdata.updates_roles()                               
                        else:
                            if role_name == 'owner':
                               await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['leadstaff', 'lead-staff']:
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'moderator':
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['cs', 'staff']:
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'tcs':
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'admin':
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'vip':
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            else:
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            
                else:
                    await message.channel.send(f">>> :arrow_right:**:x:Invalid Format! Use `{prefix}{commands_prefix}rids <role>`**")


            elif m[0] == (cmd +'rcids'):
                if len(m) == 2:
                    custom = m[1]
                    custom_mapping = {'tag': 'customtag', 'effect': 'customeffects'}

                    if custom in custom_mapping:
                        custom_field = custom_mapping[custom]
                        custom_data = pdata.get_custom()
                        if custom_data[custom_field]:
                            custom_data[custom_field] = {}
                            if custom == 'tag':
                                await message.channel.send(f">>> :arrow_right:**Successfully removed all IDs from [:reminder_ribbon:CUSTOM-TAG ] in {servers}**")
                            elif custom == 'effect':
                                await message.channel.send(f">>> :arrow_right:**Successfully removed all IDs from [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT ] in {servers}**")    
                            pdata.update_custom()
                        else:
                            if custom == 'tag':
                                await message.channel.send(f">>> :arrow_right:**pbid's are not available in [:reminder_ribbon:CUSTOM-TAG ] in {servers}**")
                            elif custom == 'effect':
                                await message.channel.send(f">>> :arrow_right:**pbid's are not available in [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT ] in {servers}**")    
                    else:
                        await message.channel.send(f">>> :arrow_right:**Invalid custom! Use `tag` and `effect`**")         
                else:
                    await message.channel.send(f">>> :arrow_right:**:x:Invalid Format! Use `{prefix}{commands_prefix}rcids <custom>`**")                         

            elif m[0] == 'rids':
                if len(m) >= 2:
                    role_name = m[1].lower()  
                    reply = ""
                    roles_data = pdata.get_roles()        
                    if role_name not in roles_data:
                        for role in roles_data:        
                            reply = reply+role+", "                  
                        await channel.send(f">>> :arrow_right:**`Use Role - {reply}`**")
                    else:
                        if roles_data[role_name]['ids']:
                            roles_data[role_name]['ids'] = []                      
                            if role_name == 'owner':
                               await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['leadstaff', 'lead-staff']:
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'moderator':
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['cs', 'staff']:
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'tcs':
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'admin':
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'vip':
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            else:
                                await channel.send(f">>> :arrow_right:**Successfully removed all ID's from [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            pdata.updates_roles()                               
                        else:
                            if role_name == 'owner':
                               await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['leadstaff', 'lead-staff']:
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'moderator':
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name in ['cs', 'staff']:
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'tcs':
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'admin':
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            elif role_name == 'vip':
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            else:
                                await message.channel.send(f">>> :arrow_right:**pbid's is not available in [ :reminder_ribbon:{role_name.upper()} ] in {servers}**")
                            
                else:
                    await message.channel.send(f">>> :arrow_right:**:x:Invalid Format! Use `{prefix}rids <role>`**")


            elif m[0] == 'rcids':
                if len(m) == 2:
                    custom = m[1]
                    custom_mapping = {'tag': 'customtag', 'effect': 'customeffects'}

                    if custom in custom_mapping:
                        custom_field = custom_mapping[custom]
                        custom_data = pdata.get_custom()
                        if custom_data[custom_field]:
                            custom_data[custom_field] = {}
                            if custom == 'tag':
                                await message.channel.send(f">>> :arrow_right:**Successfully removed all IDs from [:reminder_ribbon:CUSTOM-TAG ] in {servers}**")
                            elif custom == 'effect':
                                await message.channel.send(f">>> :arrow_right:**Successfully removed all IDs from [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT ] in {servers}**")    
                            pdata.update_custom()
                        else:
                            if custom == 'tag':
                                await message.channel.send(f">>> :arrow_right:**pbid's are not available in [:reminder_ribbon:CUSTOM-TAG ] in {servers}**")
                            elif custom == 'effect':
                                await message.channel.send(f">>> :arrow_right:**pbid's are not available in [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT ] in {servers}**")    
                    else:
                        await message.channel.send(f">>> :arrow_right:**Invalid custom! Use `tag` and `effect`**")         
                else:
                    await message.channel.send(f">>> :arrow_right:**:x:Invalid Format! Use `{prefix}rcids <custom>`**")                         
          
#### ADD CMD SECTION

            # add cmd to any role
            elif m[0] == 'bsac':
                if len(m) == 3:
                    role = m[1].lower()  
                    command = m[2]
                    reply = ""
                    roles_data = pdata.get_roles()        
                    if role not in roles_data:
                        for role in roles_data:        
                            reply = reply+role+", "                  
                        await channel.send(f">>> :arrow_right:**`Use Role - {reply}`**")
                    else:            
                         if command in roles_data.get(role, {}).get('commands', []):
                             await message.channel.send(f">>> :arrow_right:**`{m[2]}` command is already in the {role} role in {servers} :)**")
                         else:
                             roles_data[role]['commands'].append(m[2])
                             pdata.updates_roles()
                             await message.channel.send(f">>> :arrow_right:**Successfully added [ `{m[2]}` CMD ] to the {role} role in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}asac <role> <command>`**".format(prefix))

            elif m[0] == 'bsrc':
                if len(m) == 3:
                    role = m[1].lower()  
                    command = m[2]
                    reply = ""
                    roles_data = pdata.get_roles()        
                    if role not in roles_data:
                        for role in roles_data:        
                            reply = reply+role+", "                  
                        await channel.send(f">>> :arrow_right:**`Use Role - {reply}`**")
                    else:            
                         if command in roles_data.get(role, {}).get('commands', []):
                             roles_data[role]['commands'].remove(m[2])
                             pdata.updates_roles()
                             await message.channel.send(f">>> :arrow_right:**Successfully removed [ `{m[2]}` CMD ] from the {role} role in {servers}**")
                         else:
                             await message.channel.send(f">>> :arrow_right:**Command [ `{m[2]}` ] is not in the {role} role in {servers} :(**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}asrc <role> <command>`**".format(prefix))

            # add cmd to any role in specific server 
            elif m[0] == (cmd +'ac'):
                if len(m) == 3:
                    role = m[1].lower()  
                    command = m[2]
                    reply = ""
                    roles_data = pdata.get_roles()        
                    if role not in roles_data:
                        for role in roles_data:        
                            reply = reply+role+", "                  
                        await channel.send(f">>> :arrow_right:**`Use Role - {reply}`**")
                    else:            
                         if command in roles_data.get(role, {}).get('commands', []):
                             await message.channel.send(f">>> :arrow_right:**`{m[2]}` command is already in the {role} role in {servers} :)**")
                         else:
                             roles_data[role]['commands'].append(m[2])
                             pdata.updates_roles()
                             await message.channel.send(f">>> :arrow_right:**Successfully added [ `{m[2]}` CMD ] to the {role} role in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}ac <role> <command>`**".format(prefix, commands_prefix))

            elif m[0] == (cmd +'rc'):
                if len(m) == 3:
                    role = m[1].lower()  
                    command = m[2]
                    reply = ""
                    roles_data = pdata.get_roles()        
                    if role not in roles_data:
                        for role in roles_data:        
                            reply = reply+role+", "                  
                        await channel.send(f">>> :arrow_right:**`Use Role - {reply}`**")
                    else:            
                         if command in roles_data.get(role, {}).get('commands', []):
                             roles_data[role]['commands'].remove(m[2])
                             pdata.updates_roles()
                             await message.channel.send(f">>> :arrow_right:**Successfully removed [ `{m[2]}` CMD ] from the {role} role in {servers}**")
                         else:
                             await message.channel.send(f">>> :arrow_right:**Command [ `{m[2]}` ] is not in the {role} role in {servers} :(**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}rc <role> <command>`**".format(prefix, commands_prefix))

### tag and effect add cmd in specific server and all server :)))))

           #cmd to add tag from dc in any server
            elif m[0] == (cmd +'tagadd'):
                if len(m) == 3:
                    pb_id = m[1]
                    custom_tag = m[2]
                    custom_data = pdata.get_custom()

                    if pb_id in custom_data.get('customtag', {}):
                        await message.channel.send(f">>> :arrow_right:**User already has a [:reminder_ribbon:CUSTOM-TAG: `{custom_data['customtag'][pb_id]}` ] in {servers}**")
                    else:
                        custom_data['customtag'][pb_id] = custom_tag
                        pdata.update_custom()
                        await message.channel.send(f">>> :arrow_right:**Successfully added [:reminder_ribbon:CUSTOM-TAG: `{custom_tag}` ] to user [ `{pb_id}` ] in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}tagadd <pbid> <tag>`**".format(prefix, commands_prefix))
                            
 
            elif m[0] == (cmd +'tagremove'):
                if len(m) == 2:
                    pb_id = m[1]
                    custom_data = pdata.get_custom()
                    if pb_id in custom_data.get('customtag', {}):
                        del custom_data['customtag'][pb_id]
                        pdata.update_custom()
                        await message.channel.send(f">>> :arrow_right:**Successfully removed [:reminder_ribbon:CUSTOM-TAG ] from user [ `{pb_id}` ] in {servers}**")
                    else:
                        await message.channel.send(f">>> :arrow_right:**User [ `{pb_id}` ] does not have a [:reminder_ribbon:CUSTOM-TAG ] in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}tagremove <pbid>`**".format(prefix, commands_prefix))
             
          #cmd to add custom effect from dc in any server
            elif m[0] == (cmd +'effectadd'):
                if len(m) == 3:
                    pb_id = m[1]
                    custom_effect = m[2]
                    custom_data = pdata.get_custom()

                    if pb_id in custom_data.get('customeffects', {}):
                        await message.channel.send(f">>> :arrow_right:**User already has a [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT: `{custom_data['customeffects'][pb_id]}` ] in {servers}**")
                    else:
                        custom_data['customeffects'][pb_id] = custom_effect
                        pdata.update_custom()
                        await message.channel.send(f">>> :arrow_right:**Successfully added [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT: `{custom_effect}` ] to user [ `{pb_id}` ] in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}effectadd <pbid> <effect>`**".format(prefix, commands_prefix))
             
                
            elif m[0] == (cmd +'effectremove'):
                if len(m) == 2:
                    pb_id = m[1]
                    custom_data = pdata.get_custom()
                    if pb_id in custom_data.get('customeffects', {}):
                        del custom_data['customeffects'][pb_id]
                        pdata.update_custom()
                        await message.channel.send(f">>> :arrow_right:**Successfully removed [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT ] from user [ `{pb_id}` ] in {servers}**")
                    else:
                        await message.channel.send(f">>> :arrow_right:**User [ `{pb_id}` ] does not have a [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT ] in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}effectremove <pbid>`**".format(prefix, commands_prefix))
             
           #cmd to add tag in all servers
            elif m[0] == 'tagadd':
                if len(m) == 3:
                    pb_id = m[1]
                    custom_tag = m[2]
                    custom_data = pdata.get_custom()

                    if pb_id in custom_data.get('customtag', {}):
                        await message.channel.send(f">>> :arrow_right:**User already has a [:reminder_ribbon:CUSTOM-TAG: `{custom_data['customtag'][pb_id]}` ] in {servers}**")
                    else:
                        custom_data['customtag'][pb_id] = custom_tag
                        pdata.update_custom()
                        await message.channel.send(f">>> :arrow_right:**Successfully added [:reminder_ribbon:CUSTOM-TAG: `{custom_tag}` ] to user [ `{pb_id}` ] in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}tagadd <pbid> <tag>`**".format(prefix))


            elif m[0] == 'tagremove':
                if len(m) == 2:
                    pb_id = m[1]
                    custom_data = pdata.get_custom()
                    if pb_id in custom_data.get('customtag', {}):
                        del custom_data['customtag'][pb_id]
                        pdata.update_custom()
                        await message.channel.send(f">>> :arrow_right:**Successfully removed [:reminder_ribbon:CUSTOM-TAG ] from user [ `{pb_id}` ] in {servers}**")
                    else:
                        await message.channel.send(f">>> :arrow_right:**User [ `{pb_id}` ] does not have a [:reminder_ribbon:CUSTOM-TAG ] in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}tagremove <pbid>`**".format(prefix))
             
          #cmd to add custom effect in all server :)) from dc
            elif m[0] == 'effectadd':
                if len(m) == 3:
                    pb_id = m[1]
                    custom_effect = m[2]
                    custom_data = pdata.get_custom()

                    if pb_id in custom_data.get('customeffects', {}):
                        await message.channel.send(f">>> :arrow_right:**User already has a [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT: `{custom_data['customeffects'][pb_id]}` ] in {servers}**")
                    else:
                        custom_data['customeffects'][pb_id] = custom_effect
                        pdata.update_custom()
                        await message.channel.send(f">>> :arrow_right:**Successfully added [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT: `{custom_effect}` ] to user [ `{pb_id}` ] in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}effectadd <pbid> <effect>`**".format(prefix))
             
                
            elif m[0] == 'effectremove':
                if len(m) == 2:
                    pb_id = m[1]
                    custom_data = pdata.get_custom()
                    if pb_id in custom_data.get('customeffects', {}):
                        del custom_data['customeffects'][pb_id]
                        pdata.update_custom()
                        await message.channel.send(f">>> :arrow_right:**Successfully removed [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT ] from user [ `{pb_id}` ] in {servers}**")
                    else:
                        await message.channel.send(f">>> :arrow_right:**User [ `{pb_id}` ] does not have a [<a:emoji_81:1089458873825497138>CUSTOM-EFFECT ] in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}effectremove <pbid>`**".format(prefix))
             
            #important message in all servers
            elif m[0] == 'im':
                if len(m) >= 3:
                    sender_name = m[1]
                    message = " ".join(m[2:])
                    ba.internal.chatmessage(message, sender_override=sender_name)
                    await channel.send(f">>> :arrow_right:**Message has been sent as [ {sender_name}: {message} ] in all servers :)**")
                else:
                    await channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}im [server name] [important message]`**".format(prefix))
             
            #important message in anyone servers
            elif m[0] == (cmd +'im'):
                if len(m) >= 3:
                    sender_name = m[1]
                    message = " ".join(m[2:])
                    ba.internal.chatmessage(message, sender_override=sender_name)
                    await channel.send(f">>> :arrow_right:**Message has been sent as [ {sender_name}: {message} ] in {servers}**")
                else:
                    await channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}im [server name] [important message]`**".format(prefix, commands_prefix))

            #getroles of player by pbid :)))
            elif m[0] == 'getroles':
                if len(m) == 2:
                    pbid = m[1]
                    reply = ""
                    roles = pdata.get_player_roles(pbid)   
                    if roles:       
                        for role in roles:
                            reply = reply+role+", "
                        await message.channel.send(f">>> :arrow_right:**{m[1]} have [ {reply} ] role in {servers}**")
                    else:
                        await message.channel.send(f">>> :arrow_right:**{m[1]} don't have any role in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}getroles <pbid>`**".format(prefix))                    

            #getroles of player by pbid in specific server :)))
            elif m[0] == (cmd +'getroles'):
                if len(m) == 2:
                    pbid = m[1]
                    reply = ""
                    roles = pdata.get_player_roles(pbid)   
                    if roles:        
                        for role in roles:
                            reply = reply+role+", "
                        await message.channel.send(f">>> :arrow_right:**{m[1]} have [ {reply} ] role in {servers}**")
                    else:
                        await message.channel.send(f">>> :arrow_right:**{m[1]} don't have any role in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}getroles <pbid>`**".format(prefix, commands_prefix))                   
                    
           # check player tag by pbid :)))))))
            elif m[0] == (cmd +'checktag'):
                if len(m) == 2:
                    acid = m[1]
                    stats = mystats.get_all_stats()
                    roles = pdata.get_custom()['customtag']                 
                    if acid in roles:        
                        tag = roles[acid]

                        await message.channel.send(">>> :arrow_right:**:reminder_ribbon:|| TagData From: {0} **".format(servers))  
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Account-ID = `{acid}`**")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Custom-Tag = `{tag}`**")   
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Name: `{stats[acid]['name']}` **")                                   
                    else:
                        await message.channel.send(f">>> :arrow_right:**{m[1]} don't have tag in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}checktag <pbid>`**".format(prefix, commands_prefix))                    

           # check player effect by pbid :)))))))
            elif m[0] == (cmd +'checkeffect'):
                if len(m) == 2:
                    acid = m[1]
                    stats = mystats.get_all_stats()
                    roles = pdata.get_custom()['customeffects']                 
                    if acid in roles:       
                        effect = roles[acid]

                        await message.channel.send(">>> :arrow_right:**:reminder_ribbon:|| EffectData From: {0} **".format(servers))  
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Account-ID = `{acid}`**")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Custom-Effect = `{effect}`**")   
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Name: `{stats[acid]['name']}` **")                                   
                    else:
                        await message.channel.send(f">>> :arrow_right:**{m[1]} don't have effect in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}checkeffect <pbid>`**".format(prefix, commands_prefix))                    

           # player data by pbid :)
            elif m[0] == (cmd +'pdata'):
                if len(m) == 2:
                    ac_id = m[1]
                    stats = mystats.get_all_stats()
                    if ac_id in stats:
                        ac = m[1]
                        coins = nc.getcoins(ac)
                        
                        await message.channel.send(">>> :arrow_right:**:reminder_ribbon:|| PlayerData From: {0} **".format(servers))  
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Name: {stats[ac_id]['name']} **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Account ID: {ac_id} **")                        
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Coins: {coins} <:CoinBank:1201395254360813609> **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Rank: {stats[ac_id]['rank']} **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Score: {stats[ac_id]['scores']} **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Kills: {stats[ac_id]['kills']} **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Deaths: {stats[ac_id]['deaths']} **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Kd_Score: {stats[ac_id]['kd']} **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Last Seen: {stats[ac_id]['last_seen']} **")    
                    else:
                        await message.channel.send(f">>> :arrow_right:**{m[1]} Not played in {servers} yet**")   
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}pdata <pbid>`**".format(prefix, commands_prefix))                                     

            #retrieve the info of device id and ip by pb id :)
            elif m[0] == (cmd +'bandata'):
                if len(m) == 2:
                    ac_id = m[1]
                    ban = pdata.get_profiles()                  
                    if ac_id in ban:
                        ip = ban[ac_id]["lastIP"]
                        device_id = ban[ac_id]["deviceUUID"]
                        account_age = ban[ac_id]["accountAge"]
                        otheraccounts = pdata.get_detailed_pinfo(ac_id)
                        
                        await message.channel.send(">>> :arrow_right:**:reminder_ribbon:|| BanData From: {0} **".format(servers))                       
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Name: {ban[ac_id]['name']} **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Account ID: {ac_id} **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| IP: {ip} **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Device-id: {device_id} **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Linked Account: {otheraccounts} **")
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Account-Age: {account_age} **")     
                        await message.channel.send(f">>> :arrow_right:**:reminder_ribbon:|| Last msg: {ban[ac_id]['lastMsg']} **")                        
                    else:
                        await message.channel.send(f">>> :arrow_right:**{m[1]} Not played in {servers} yet**")   
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}{1}dinfodata <pbid>`**".format(prefix, commands_prefix))                                     

            # get top 10 player list xD
            elif m[0] == (cmd +'top10'):
                stats = mystats.get_all_stats()

                #print("Debug: Stats content before sorting:", stats)

                if stats:    
                        sorted_players = sorted(stats.items(), key=lambda x: x[1].get('rank', float('inf')))
                        top_10_players = sorted_players[:10]
                        top_10_message = ">>> :reminder_ribbon:**Top 10 Players of {0}:**\n".format(servers)
                        
                        for rank, (player_id, player_data) in enumerate(top_10_players, start=1):
                            player_name = player_data.get('name', 'Unknown')
                            player_accountid = player_data.get('aid', 'N/A')
                            player_scores = player_data.get('scores', 'N/A')
                            player_kd = player_data.get('kd', 'N/A')
                            top_10_message += (f"{rank}).:reminder_ribbon:| Account-ID: {player_accountid}, Name: {player_name}, Score: {player_scores}, KD-Score: {player_kd}\n")                        
                        await message.channel.send(top_10_message)
                        
                else:
                    await message.channel.send(">>> Stats information not available.")


            elif m[0] == 'aeffectlist':                  
                await message.channel.send(">>> <a:emoji_81:1089458873825497138>**__EFFECTS LIST__** :-\n:reminder_ribbon:| **NORMAL-EFFECTS - spark, sparkground, shine, ice, sweat, sparkground, sweatground, scorch, ice, splinter, highlightshine, iceground, glow, distortion, slime, metal, surrounder, brust, colorfullspark**\n:reminder_ribbon:| **PREMIUM-EFFECTS - fairydust, stars, new_rainbow, chispitas, ring, darkmagic, footprint, fire**")

        #--------------------------------------------------------------------------------------------------------------------
            if m[0] == 'useradd':
                if len(m) == 2:   
                    user_id = int(m[1])                
                    settings = setting.get_settings_data()
                   
                    if int(m[1]) in settings.get('discordbot', {}).get('allowed_user_ids', []):
                        await message.channel.send(f">>> :arrow_right:**User is already in the allowed list in {servers}**")
                    else:
                        
                        settings['discordbot']['allowed_user_ids'].append(int(m[1]))
                        with open(setting_json_path, 'w') as file:
                            json.dump(settings, file, indent=4)
                        
                        user = await client.fetch_user(user_id)
                        username = user.name if user else f"Unknown User ({user_id})"


                        await message.channel.send(f">>> :arrow_right:**Successfully added user `{username}` (ID: `{user_id}`) to the allowed list in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}useradd <userid>`**".format(prefix))

            if m[0] == 'userremove':
                if len(m) == 2:
                    user_id = int(m[1])
                    settings = setting.get_settings_data()

                    if int(m[1]) in settings.get('discordbot', {}).get('allowed_user_ids', []):
                        settings['discordbot']['allowed_user_ids'].remove(int(m[1]))
                        with open(setting_json_path, 'w') as file:
                            json.dump(settings, file, indent=4)
                        user = await client.fetch_user(user_id)
                        username = user.name if user else f"Unknown User ({user_id})"


                        await message.channel.send(f">>> :arrow_right:**Successfully removed user  `{username}`(ID : `{user_id}`) from the allowed list in {servers}**")
                    else:
                        await message.channel.send(f">>> :arrow_right:**User ID `{user_id}` is not in the allowed list in {servers}**")
                else:
                    await message.channel.send(">>> :arrow_right:**:x:Invalid Format! Use `{0}userremove <userid>`**".format(prefix))



  
@client.event
async def on_ready():
    print("Connected to discord: %s [%s]" %
          (client.user.name, client.user.id))
    await verify_channel()


async def verify_channel():
    global livestatsmsgs
    channel = client.get_channel(liveStatsChannelID)
    botmsg_count = 0
    msgs = []
    async for msg in channel.history(limit=5):
        if msg.author.id == client.user.id:
            botmsg_count += 1
            livestatsmsgs.append(msg)

    livestatsmsgs.reverse()
    while (botmsg_count < 1):
        new_msg = await channel.send(embed=discord.Embed(title='Fetching messages! Please wait!'))
        livestatsmsgs.append(new_msg)
        botmsg_count += 1
    asyncio.run_coroutine_threadsafe(refresh_stats(), client.loop)
    asyncio.run_coroutine_threadsafe(send_logs(), client.loop)

async def refresh_stats():
    global stats
    await client.wait_until_ready()

    while not client.is_closed():
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        ip = _ba.our_ip
        port = _ba.our_port
        #serverping = ping.get_game_server_ping(ip)
        reset = _ba.season_ends_in_days
        server = _ba.app.server._config.party_name
        size = mid.members
        msg = ''
        try:
            for id in stats['roster']:
                name = stats['roster'][id]['name']
                device_id = stats['roster'][id]['device_id']
                msg = msg + f"[{id}] {name} {device_id}\n"
        except Exception as err:
            print(f"ERROR OCCURED IN BOT.PY:\n{err}")
    
        embed=discord.Embed(title="", description=f"### {server} \n\n\n```ocaml\nCurrent Game: {stats['playlist']['current']}\nNext Game: {stats['playlist']['next']}```")
        embed.set_author(name="LIVE SERVER STATUS | NODE #1", icon_url="https://cdn.discordapp.com/emojis/878301194865508422.gif?size=512")
        embed.add_field(name=" **Players Registred**", value=f"```py\nMEMBERS_COUNT = {len(size)} ```", inline=False)
        embed.add_field(name=" **Server's Reset**", value=f"```py\nSEASON ENDS IN {reset} DAYS```", inline=True)
        embed.add_field(name=" **Server's Info**", value=f"```py\nIP = {ip} \nPORT = {port} ```", inline=False)    
        embed.add_field(name=" **Players**", value=f"```py\n{len(stats['roster'])}/{ba.internal.get_public_party_max_size()} ```", inline=True)
        embed.add_field(name=" **Public**", value=f"```py\n{ba.internal.get_public_party_enabled()} ```", inline=True)
        embed.add_field(name=" **Ping**", value=f"```yaml\nSoon.... ```", inline=True)
        embed.add_field(name="**PLAYERS IN SERVER:**", value=f"```\n{msg if len(msg) != 0 else 'I am alone.. :('}```", inline=False)
        #embed.add_field(name="CPU STATUS:", value="\u200b", inline=False)
        embed.add_field(name="RAM", value=f"```\n{ram}%```", inline=True)
        embed.add_field(name="CPU", value=f"```\n{cpu}%```", inline=True)
        embed.add_field(name="TOP 5 PLAYERS", value=f"1.{mystats.top5Name[0]}\n2.{mystats.top5Name[1]}\n3.{mystats.top5Name[2]}\n4.{mystats.top5Name[3]}\n5.{mystats.top5Name[4]}", inline=False)
        embed.set_footer(text="Auto updates every 10 seconds!", icon_url='https://cdn.discordapp.com/emojis/842886491533213717.gif?size=96&quality=lossless')
        await livestatsmsgs[0].edit(embed=embed)
        await asyncio.sleep(10)


async def send_logs():
    global logs
    # safely dispatch logs to dc channel , without being rate limited and getting ban from discord
    # still we sending 2 msg and updating 2 msg within 5 seconds , umm still risky ...nvm not my problem
    channel = client.get_channel(logsChannelID)
    await client.wait_until_ready()
    while not client.is_closed():
        if logs:
            msg = ''
            for msg_ in logs:
                msg += msg_+"\n"
            logs = []
            if msg:
                #await requests.post("https://discord.com/api/webhooks/1088893756822011976/BSZFLkbB4VXYe-bo_6yD4CzfGdWGmy40xHmlqBx4sfI5QSH7axhKpj8g69rR486lBfpm", json = msg)
                await channel.send(msg)
        await asyncio.sleep(10)

class BsDataThread(object):
    def __init__(self):
        self.refreshStats()
        self.Timer = ba.Timer(8, ba.Call(self.refreshStats), repeat=True)
        #self.Timerr = ba.Timer( 10,ba.Call(self.refreshLeaderboard),timetype = ba.TimeType.REAL,repeat = True)

    #def refreshLeaderboard(self):
         #global leaderboard
         #global top200
         #_t200={}
         #f=open(statsfile)
         #lboard=json.loads(f.read())
         #leaderboard=lboard
         #entries = [(a['scores'], a['kills'], a['deaths'], a['games'], a['name_html'], a['aid'],a['last_seen']) for a in lboard.values()]

         #entries.sort(reverse=True)
         #rank=0
         #for entry in entries:
         #    rank+=1
         #    if rank >201:
         #        break
         #    _t200[entry[5]]={"rank":rank,"scores":int(entry[0]),"games":int(entry[3]),"kills":int(entry[1]),"deaths":int(entry[2]),"name_html":entry[4],"last_seen":entry[6]}
         #    top200=_t200

    def refreshStats(self):

        liveplayers = {}
        nextMap = ''
        currentMap = ''
        global stats

        for i in ba.internal.get_game_roster():
            try:
                liveplayers[i['account_id']] = {
                    'name': i['players'][0]['name_full'], 'client_id': i['client_id'], 'device_id': i['display_string']}
            except:
                liveplayers[i['account_id']] = {
                    'name': "<in-lobby>", 'clientid': i['client_id'], 'device_id': i['display_string']}
        try:
            nextMap = ba.internal.get_foreground_host_session(
            ).get_next_game_description().evaluate()

            current_game_spec = ba.internal.get_foreground_host_session()._current_game_spec
            gametype: Type[GameActivity] = current_game_spec['resolved_type']

            currentMap = gametype.get_settings_display_string(
                current_game_spec).evaluate()
        except:
            pass
        minigame = {'current': currentMap, 'next': nextMap}
        #system={'cpu':p.cpu_percent(),'ram':p.virtual_memory().percent}
        #system={'cpu':80,'ram':34}
        #stats['system']=system
        stats['roster'] = liveplayers
        stats['chats'] = ba.internal.get_chat_messages()
        stats['playlist'] = minigame
        #stats['teamInfo']=self.getTeamInfo()
