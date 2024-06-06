from .Handlers import send, sendall, sendchat
import ba,os
import _ba,json
from features import discord_bot as dc
from datetime import datetime, timedelta
import discord, requests, asyncio
from playersData import pdata
import setting 
import ba.internal
from stats import mystats
from ba._general import Call
import _thread
import setting
settings = setting.get_settings_data()
ticket = settings["CurrencyType"]["CurrencyName"]
tic = settings["CurrencyType"]["Currency"] #dont change this or it will give an error

Commands = ['me', 'list', 'uniqeid', 'ping', 'vp', 'uid', 'pbid', 'comp', 'complaintstep']
CommandAliases = ['stats', 'score', 'rank',
                  'myself', 'l', 'id', 'link', 'pb-id', 'dclink', 'pb', 'accountid', 'coinhelp', 'voting-playlist', 'complaint', 'cs']


def ExcelCommand(command, arguments, clientid, accountid, ARGUMENTS):
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
    if command in ['me', 'rank', 'stats', 'score', 'myself']:
        fetch_send_stats(accountid, clientid)

    elif command in ['list', 'l']:
        list(clientid)

    elif command in ['uniqeid', 'uid', 'pb-id', 'pbid', 'accountid']:
        accountid_request(arguments, clientid, accountid)

    elif command in ['id', 'pb']:
        accountid_clientid(arguments, clientid, accountid)

    elif command in ['ping']:
        get_ping(arguments, clientid)

    elif command in ['voting-playlist', 'vp']:
        voting_playlist(arguments, clientid)

    elif command in ['cs', 'complaintstep']:
        complaint_step(arguments, clientid)
        
    elif command == 'coinhelp':
        coinhelp(arguments, clientid)

    elif command == 'link':
        linked_user(arguments, clientid, accountid)
        
    elif command in ['comp', 'complaint']:
        get_complaint(arguments, clientid, accountid, ARGUMENTS)

    elif command == 'dclink':
        linkingdc(arguments, clientid)       


def get_ping(arguments, clientid):
    if arguments == [] or arguments == ['']:
        send(f"Your ping {_ba.get_client_ping(clientid)}ms ", clientid)
    elif arguments[0] == 'all':
        pingall(clientid)
    else:
        try:
            session = ba.internal.get_foreground_host_session()

            for index, player in enumerate(session.sessionplayers):
                name = player.getname(full=True, icon=False),
                if player.inputdevice.client_id == int(arguments[0]):
                    ping = _ba.get_client_ping(int(arguments[0]))
                    send(f" {name}'s ping {ping}ms", clientid)
        except:
            return

#added tickets in stats :))
def getcoins(account_id: str):
  BANK_PATH = _ba.env().get("python_directory_user", "") + "/bank.json"
  with open(BANK_PATH, 'r') as f:
     coins = json.loads(f.read())
     if account_id in coins:
         return coins[account_id]

def stats(ac_id, clientid):
    stats = mystats.get_stats_by_id(ac_id)
    if stats:
        tickets = getcoins(ac_id)
        reply = (
            f"\ue048| Name: {stats['name']}\n"
            f"\ue048| PB-ID: {stats['aid']}\n"
            f"\ue048| {ticket.capitalize()}: {tickets}{tic}\n"
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


def fetch_send_stats(ac_id, clientid):
    _thread.start_new_thread(stats, (ac_id, clientid,))


def pingall(clientid):
    """Returns The List Of Players Clientid and index"""

    p = u'{0:^16}{1:^34}ms'
    seprator = '\n______________________________\n'

    list = p.format('Name', 'Ping (ms)')+seprator
    session = ba.internal.get_foreground_host_session()

    for index, player in enumerate(session.sessionplayers):
        list += p.format(player.getname(icon=True),
                         _ba.get_client_ping(int(player.inputdevice.client_id)))+"\n"

    send(list, clientid)

def list(clientid):
    """Returns The List Of Players Clientid and index"""

    p = u'{0:^16}{1:^15}{2:^10}'
    seprator = '\n______________________________\n'

    list = p.format('Name', 'Client ID', 'Player ID')+seprator
    session = ba.internal.get_foreground_host_session()

    for index, player in enumerate(session.sessionplayers):
        list += p.format(player.getname(icon=False),
                         player.inputdevice.client_id, index)+"\n"

    send(list, clientid)


def voting_playlist(arguments, clientid):
    """Voting playlist list"""

    if arguments == [] or arguments == ['']:
        send(f"\ue048| VOTING GAMES LISTS ", clientid)
        send(f"\ue048| PLAYLIST EPIC SMASH TYPE PES ", clientid)
        send(f"\ue048| PLAYLIST EPIC TEAMS TYPE PET ", clientid)
        send(f"\ue048| PLAYLIST DEFAULTS GAMES TYPE PDG ", clientid)
        send(f"\ue048| PLAYLIST DEATHMATCH AND ELIMINATION ONLY TYPE PDEG ", clientid)


def complaint_step(arguments, clientid):
    """Voting playlist list"""

    if arguments == [] or arguments == ['']:
        send(f"\ue048| COMPLAINTS STEPS: ", clientid)
        send(f"\ue048| Type /complaint (clientid of offender) (complaint) or", clientid)
        send(f"\ue048| /comp (clientid of offender) (complaint)", clientid)
        send(f"\ue048| For Example: /comp 113 betraying etc!!. ", clientid)
        send(f"\ue048| Your Complaint will get sent to discord server immediately!!", clientid)
        send(f"Note - Don't spam with this command or u will get a ban permanently..!!!!!", clientid)


def coinhelp(arguments, clientid):
        send(f"\ue048|  COINSYSTEM CMDz", clientid)
        send(f"\ue048| Type /shop effects to know which effects are available to buy", clientid)
        send(f"\ue048| Type /jct to check next join claim time", clientid)
        send(f"\ue048| Type /rpe to remove paid effect..", clientid)
        send(f"\ue048| Type /buy (effect) to buy effects ", clientid)
        send(f"\ue048| Type /donate (amount of {ticket}) (clientid of player) to donate your {ticket} to a player", clientid)        
        send(f"\ue048| Type /stc (amount) to convert score to cash (not available)", clientid)
        send(f"\ue048| Type /cts (amount) to convert cash to score (not available)", clientid)
    
       
def linkingdc(arguments, clientid):
    """Linking pbid to discord-id Step"""

    if arguments == [] or arguments == ['']:
        send(f"\ue048|  LINKING PBIDs TO DISCORD IDs STEPS:", clientid)
        send(f"\ue048| Type /link (Discord user ID or Username) to link your PBID.", clientid)
        send(f"\ue048| If a user successfully links their PBID to their Discord-ID......", clientid)
        send(f"\ue048| Note: The linking process is valid only for 5 min.", clientid)

       
def accountid_request(arguments, clientid, accountid):
    """Returns The Account Id Of Players"""

    if arguments == [] or arguments == ['']:
        send(f"Your account id is {accountid} ", clientid)

    else:
        try:
            session = ba.internal.get_foreground_host_session()
            player = session.sessionplayers[int(arguments[0])]

            name = player.getname(full=True, icon=True)
            accountid = player.get_v1_account_id()

            send(f" {name}'s account id is '{accountid}' ", clientid)
        except:
            return


def accountid_clientid(arguments, clientid, accountid):
 """accountid request by clientid """
 players = _ba.get_foreground_host_activity().players
 session = ba.internal.get_foreground_host_session()
 player = _ba.get_foreground_host_activity()
 a = arguments
 with ba.Context(player):
   if True:
      clld = int(a[0])
      for i in session.sessionplayers:
          if i.inputdevice.client_id == clld:
              names = i.getname(full=True, icon=True)
              accountid = i.get_v1_account_id()
              send(f" {names}'s account id is '{accountid}' ", clientid)

  
def linked_user(arguments, clid, acid):
    player = _ba.get_foreground_host_activity()    
    if not arguments or arguments == ['']:
        with ba.Context(player):
            send(f"Using: /link [DC user-ID or Dc User-Name]", clid)
    else:
        userid = arguments[0]
        send(f"\ue048| Please wait.. Fetching your Discord info", clid)
        asyncio.ensure_future(dc.link_pbid_to_discord(user_id_or_name=userid,pbid=acid,clientid=clid))


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

                    settime = settings["complaintTimeoutInHours"]
                    expiry = datetime.now() + timedelta(hours=settime)
                    customers[acid] = {'expiry': expiry.strftime('%d-%m-%Y %I:%M:%S %p')}
                    
                    # Call the send_complaint_to_channel function                
                    asyncio.ensure_future(dc.send_complaint_to_channel(server_name=server, time=now, myself=myself, ign=name, useracid=acid, fign=fname, acid=pbid, linkedaccount=otheraccounts, offender=offendr, complaint=complaint))
                    
                    send("A complaint has been sent on the Discord server. Please wait for Staff to take action...!!", clientid)
                else:
                    till = customers[acid]['expiry']
                    send(f"You can use the complaint command again at {till}", clientid)
