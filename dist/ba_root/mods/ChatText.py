import _ba,ba
import random
import setchat
#you will need settings.py from our repository
messagelist = setchat.messagelist

def message():
    keys = []
    for x in messagelist:
        keys.append(x)
    messages = keys[randrange(len(keys))]
    _ba.chatmessage(messages)
    return

cmt = setchat.chatmessagetime
if setchat.allow: 
    ba.Timer(cmt, ba.Call(message), timetype=ba.TimeType.REAL, repeat=True)
    print("message sender working...")
