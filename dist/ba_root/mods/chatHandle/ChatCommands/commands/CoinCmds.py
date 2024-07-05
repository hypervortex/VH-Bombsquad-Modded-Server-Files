from .Handlers import handlemsg, handlemsg_all, send, clientid_to_myself, sendchat
from playersData import pdata
# from tools.whitelist import add_to_white_list, add_commit_to_logs
from serverData import serverdata
import ba,os,json
from datetime import datetime, timedelta
import _ba
import time
import setting
import ba.internal
import _thread
import set
import random
import setting
from stats import mystats
from bastd.gameutils import SharedObjects
from tools import playlist
from tools import logger, mongo
import set
import threading
import json
Commands = ['cjt', 'checkjointime', 'shop', 'donate','removepaideffect']
CommandAliases = ['give', 'buy', 'cts', 'stc', 'rpe', 'scoretocash', 'cashtoscore']

BANK_PATH = _ba.env().get("python_directory_user", "") + "/bank.json"
base_path = os.path.join(_ba.env()['python_directory_user'], "stats" + os.sep)
statsfile = base_path + 'stats.json'
python_path = _ba.env()["python_directory_user"]
settings = setting.get_settings_data()
ticket = settings["CurrencyType"]["CurrencyName"]
tic = settings["CurrencyType"]["Currency"] #dont change this or it will give an error



def CoinCommands(command, arguments, clientid, accountid):
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
    if command == 'shop':
       shop(arguments, clientid)

    elif command in ['scoretocash', 'stc']:
        stc(arguments, clientid, accountid)

    elif command in ['cashtoscore', 'cts']:
        cts(arguments, clientid, accountid)
 
    elif command in ['donate', 'give']:
        donate(arguments, clientid, accountid)

    elif command == 'buy':
        buy(arguments, clientid, accountid)

    elif command in ['rpe', 'removepaideffect']:
        rpe(arguments, clientid, accountid)

    elif command in ['cjt', 'checkjointime']:
        check_claim_time(arguments, clientid, accountid)
       

def getcoins(accountid: str):
  with open(BANK_PATH, 'r') as f:
     coins = json.loads(f.read())
     if accountid in coins:
         return coins[accountid]

def getstats():
    f = open(statsfile, 'r')
    return json.loads(f.read())


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
        ba.playsound(ba.getsound("cashRegister"))
    #print('Transaction successful')

def addcoin(accountid: str, amount: int):
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


def shop(arguments, clientid):
    players = _ba.get_foreground_host_activity().players
    player = _ba.get_foreground_host_activity()
    a = arguments
    with ba.Context(player):
        string = '==You can buy following items==\n'
        if a == []:
            send("Usage: /shop commands, /shop effects", clientid)
        elif a[0].startswith('effects'):
            for x in set.availableeffects:
                string += f"{x} ---- {tic}{str(set.availableeffects[x])} ---- for 1 day\n"
            send(string, clientid)
        elif a[0].startswith('commands'):
            separator = '          '
            for x in set.availablecommands:
                string += f"{x}----{tic}{str(set.availablecommands[x])}{separator}"
                if separator == '          ': separator = '\n'
                else: separator = '          '
                ba.screenmessage(string, transient=True, color=(1, 1, 1), clients=[clientid])
        else:
            send("Usage: /shop commands or /shop effects", clientid)


def check_claim_time(arguments, clientid, accountid):
    customers = pdata.get_custom()['coin_claim']
    if accountid in customers:
        if customers:
            expiry = datetime.strptime(customers[accountid]['expiry'], '%d-%m-%Y %H:%M:%S')
            remaining_time_seconds = int((expiry - datetime.now()).total_seconds())

            # Calculate hours, minutes, and seconds
            hours = remaining_time_seconds // 3600
            minutes = (remaining_time_seconds % 3600) // 60
            seconds = remaining_time_seconds % 60
            send(f"Time remaining until your next join coin claim: {hours}:{minutes}:{seconds}", clientid)


def stc(arguments, clientid, accountid):
    players = _ba.get_foreground_host_activity().players
    player = _ba.get_foreground_host_activity()
    a = arguments
    with ba.Context(player, exit_result=None):
        try:
            score = int(a[0])
            stats = mystats.get_all_stats()
            havescore = stats[accountid]['scores']
            if havescore < score:
                send(f"Not enough scores to perform the transaction", clientid)
                send(f"You have {havescore} Score only....", clientid)
            elif score < 500:
                send(f"You can only convert more than 500 scores", clientid)
            else:
                stats[accountid]['scores'] -= score
                equivalentCoins = int(score / 5 * 0.9)
                addcoins(accountid, equivalentCoins)
                mystats.dump_stats(stats)
                ba.screenmessage('Transaction Successful', color=(0,1,0))           
                _ba.chatmessage(f"{str(equivalentCoins)}{tic} added to your account. [10% transaction fee deducted]")
                thread=threading.Thread(target=mystats.refreshStats)
                thread.start()
        except:
            send("Usage: /scoretocash or stc amount_of_score", clientid)

def cts(arguments, clientid, accountid):
    players = _ba.get_foreground_host_activity().players
    player = _ba.get_foreground_host_activity()
    a = arguments
    with ba.Context(player, exit_result=None):
        try:
            coins = int(a[0])
            havecoins = getcoins(accountid)
            if havecoins < coins:
                send(f"Not enough {tic}{ticket} to perform the transaction", clientid)
                send(f"You have {havecoins}{tic} only....", clientid)
            elif coins < 100:
                send(f"You can only convert more than 100{tic}", clientid)
            else:
                addcoins(accountid, coins * -1)
                stats = mystats.get_all_stats()
                equivalentScore = int(coins * 5 * 0.9)
                stats[accountid]['scores'] += equivalentScore
                mystats.dump_stats(stats)
                ba.playsound(ba.getsound("cashRegister"))
                ba.screenmessage(f'Transaction Successful', color=(0,1,0))
                _ba.chatmessage(f"{str(equivalentScore)} scores added to your account stats. [10% transaction fee deducted]")
                thread=threading.Thread(target=mystats.refreshStats)
                thread.start()
        except:
            send("Usage: /cashtoscore or cts amount_of_cash", clientid)


def donate(arguments, clientid, accountid):
  players = _ba.get_foreground_host_activity().players
  player = _ba.get_foreground_host_activity()
  session = ba.internal.get_foreground_host_session()   
  a = arguments
  with ba.Context(player):
       try:
           if len(a) < 2: 
               ba.screenmessage("Usage: /donate [amount] [clientid of player]", transient=True, clients=[clientid])
           else:
               havecoins = getcoins(accountid)
               transfer = int(a[0])
               if transfer < 100:
                   send(f"You can only transfer more than 100{tic}.", clientid)
                   return    
               sendersID = accountid
               receiversID = None  
               for i in session.sessionplayers:
                   if i.inputdevice.client_id == int(a[1]):    
                      receiversID = i.get_v1_account_id()
                      pname = i.getname(full=True, icon=True)
                   if i.inputdevice.client_id == clientid:
                      name = i.getname(full=True, icon=True)
               if None not in [sendersID, receiversID]:
                   if sendersID == receiversID: 
                        send(f"You can't transfer to your own account", clientid)  
                   elif getcoins(sendersID) < transfer: 
                        send(f"Not enough {tic}{ticket} to perform the transaction", clientid)
                        send(f"You have {havecoins}{tic} only....", clientid)
                   else:
                        addcoins(sendersID, transfer * -1)
                        addcoins(receiversID, transfer)
                        ba.playsound(ba.getsound("cashRegister"))
                        ba.screenmessage(f'Transaction Successful', color=(0,1,0))
                        _ba.chatmessage(f"Successfully transfered {transfer}{tic} into {pname}'s account.")
               else:
                   send(f"player not found", clientid)   
       except Exception as e:
           print(f"An error occurred: {e}")
           ba.screenmessage('An error occurred. Check the console for details.', transient=True, clients=[clientid])     

 
def buy(arguments, clientid, accountid):
  global effectCustomers
  players = _ba.get_foreground_host_activity().players
  player = _ba.get_foreground_host_activity()
  a = arguments
  with ba.Context(player):
   if a == []:      
       _ba.chatmessage('Usage: /buy item_name')
   elif a[0] in set.availableeffects:
       effect = a[0]
       costofeffect = set.availableeffects[effect]
       havecoins = getcoins(accountid)
       if havecoins >= costofeffect:
           customers = pdata.get_custom()['paideffects']
           if accountid not in customers:
               setdate = settings["Paideffects"]["timedelta"]
               settime = int(settings["Paideffects"]["ExpriyPaideffectTime"])
               # Map unit string to timedelta attribute
               unit_map = {'years': 'years', 'days': 'days', 'hours': 'hours', 'minutes': 'minutes', 'seconds': 'seconds'}
               if setdate in unit_map:
                   setdate_attr = unit_map[setdate]
                   expiry = datetime.now() + timedelta(**{setdate_attr: settime})
                   customers[accountid] = {'effect': effect, 'expiry': expiry.strftime('%d-%m-%Y %H:%M:%S')}
                   addcoins(accountid, costofeffect * -1)         
                   _ba.chatmessage(f"Success! That cost you {str(costofeffect)}{tic}")
               else:
                   _ba.chatmessage("Invalid timedelta unit in settings.")     
           else:
               activeeffect = customers[accountid]['effect']
               till = customers[accountid]['expiry']
               send(f"You already have {activeeffect} effect active\nTill = {till}", clientid)
       else:
           send(f"You need {str(costofeffect)}{tic} for that, You have {str(havecoins)}{tic} only.", clientid)
   else: send(f"invalid item, try using '/shop effects", clientid)


def rpe(arguments, clientid, accountid):
    try:
        custom = pdata.get_custom()['paideffects']
        aeffect = custom[accountid]['effect']
        session = ba.internal.get_foreground_host_session()
        pdata.remove_paid_effect(accountid)
        send(f"paid {aeffect} effect have been removed Successfully", clientid)
    except:
        return
