tag_customers = {}

import _ba,ba,os,json
import set
from set import *
from random import randrange
from playersData import pdata
from datetime import datetime
from typing import List, Sequence, Optional, Dict, Any
from ba._enums import SpecialChar

python_path = _ba.env()["python_directory_user"]
bankFile = python_path +'/bank.json'

correctAnswer = None
answeredBy = None
bankfile = bankFile

 
def askQuestion():
    global answeredBy
    global correctAnswer
    keys = []
    for x in set.questionsList:
        keys.append(x)
    question = keys[randrange(len(keys))]
    correctAnswer = set.questionsList[question]
    if question == 'add':
        a = randrange(100, 999)
        b = randrange(10, 99)
        correctAnswer = [str(a + b)]
        question = f'What is {str(a)} + {str(b)}?'
    elif question == 'multiply':
        a = randrange(100, 999)
        availableB = [0, 1, 2, 5, 10]
        b = availableB[randrange(4)]
        correctAnswer = [str(a * b)]
        question = f'What is {str(a)} x {str(b)}?'
    _ba.chatmessage(question)
    answeredBy = None
    return


def checkAnswer(msg: str, client_id: int):
    global answeredBy
    if True:#msg.lower() in correctAnswer:
        if answeredBy is not None:
            _ba.chatmessage(f'Already awarded to {answeredBy}.')
        else:
            ros = _ba.get_game_roster()
            for i in ros:
                if (i is not None) and (i != {}) and (i['client_id'] == client_id):
                    answeredBy = i['players'][0]['name']
                    accountID = i['account_id']
                    ba.screenmessage(f"{answeredBy}: {msg}", color=(0,0.6,0.2), transient=True)
            try:
                ticket = u'\ue01f'
                _ba.chatmessage(f"Congratulations {answeredBy}!, You won {ticket}10.")
                addCoins(accountID, 10)
            except:
                pass
    return


def addCoins(accountID: str, amount: int):
    if os.path.exists(bankfile):
        with open(bankfile) as f:
            bank = json.loads(f.read())
    else:
        bank = {}
    if accountID not in bank:
        bank[accountID] = 0
    bank[accountID] += amount
    with open(bankfile, 'w') as f:
        f.write(json.dumps(bank))
    if amount > 0:
        ba.playsound(ba.getsound('cashRegister'))
    #print("Transaction successful")


def getCoins(accountID: str):
  if os.path.exists(bankfile):
    with open(bankfile, 'r') as f:
        coins = json.loads(f.read())
        if accountID in coins:
            return coins[accountID]
  return 0


cstimer = None
if set.coin: 
    ba.Timer(set.questionDelay, ba.Call(askQuestion), timetype=ba.TimeType.REAL, repeat=True)
    print("Coin system loaded...")

def checkSettings():
    global cstimer
    if (set.coin) and set.askQuestions and (cstimer == None):
        cstimer = ba.Timer(set.questionDelay, ba.Call(askQuestion), timetype=ba.TimeType.REAL, repeat=True)
    if not set.coin and not set.askQuestions:
        cstimer = None
checkTimer = ba.Timer(5, ba.Call(checkSettings), timetype=ba.TimeType.REAL, repeat=True)

