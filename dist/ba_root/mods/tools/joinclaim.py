#ba meta requires api 7
#JoinClaim by SARA 
import ba, _ba
import random
from datetime import datetime, timedelta
from chatHandle.ChatCommands.commands import CoinCmds as cc
from chatHandle.ChatCommands.commands.Handlers import sendchatclid
from playersData import pdata

def join_claim(name, clid, accountid):
    set_time_hours = 24  # 24 hours
    set_time_seconds = set_time_hours * 3600  # Convert hours to seconds
    customers = pdata.get_custom()['coin_claim']

    if accountid not in customers:
        if set_time_seconds < 40:
            coin_claim = random.choice([50, 70, 80])  # Higher value for shorter claim times
        else:
            coin_claim = random.choice([50, 60])  # Standard values for 24 hours

        expiry = datetime.now() + timedelta(seconds=set_time_seconds)
        customers[accountid] = {'name': name, 'expiry': expiry.strftime('%d-%m-%Y %H:%M:%S')}
        tic = u'\U0001FA99'

        if coin_claim == 50:
            message = f"Congratulations,{name}You've claimed..! {coin_claim}{tic}.\n"
        elif coin_claim == 60:
            message = f"Wow, {name}You've claimed {coin_claim}{tic}.Nice..! \n"
        elif coin_claim == 70:
            message = f"Incredible,{name}!You've claimed {coin_claim}{tic}.\n"
        elif coin_claim == 80:
            message = f"{name},you're on fire..! You've claimed {coin_claim}{tic}.\n"

        cc.addcoins(accountid, coin_claim)
        sendchatclid(message, clid)

        # Add countdown message only once
        countdown_message = f"To check next join claim time: type /cjt or /checkjointime"
        sendchatclid(countdown_message, clid)
