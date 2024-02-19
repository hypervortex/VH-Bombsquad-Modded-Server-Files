from .Handlers import send, sendall, sendchat
import ba,os
import _ba,json
import ba.internal
from stats import mystats
from ba._general import Call
import _thread
Commands = ['me', 'list', 'uniqeid', 'ping']
CommandAliases = ['stats', 'score', 'rank',
                  'myself', 'l', 'id', 'pb-id', 'pb', 'accountid']


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
    if command in ['me', 'stats', 'score', 'rank', 'myself']:
        fetch_send_stats(accountid, clientid)

    elif command in ['list', 'l']:
        list(clientid)

    elif command in ['uniqeid', 'id', 'pb-id', 'pb', 'accountid']:
        accountid_request(arguments, clientid, accountid)

    elif command in ['ping']:
        get_ping(arguments, clientid)


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

    _ba.pushcall(Call(sendchat, reply), from_other_thread=True)



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
