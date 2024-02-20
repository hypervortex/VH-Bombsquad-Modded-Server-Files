# -*- coding: utf-8 -*-
# ba_meta require api 6

import _ba,ba,os,json,random,bastd
from typing import List, Sequence, Optional, Dict, Any
from datetime import datetime

path = 'mods' #'python'
#Don't change the below 4 lines
directories = [_ba.env()['python_directory_user'], _ba.env()['python_directory_app']]
python_path = None
if path == 'mods': python_path = directories[0]
if path == 'python': python_path = directories[1]
step = os.sep

#Edit the File Paths according to ur need...
#
htmlFile = f"{python_path}{step}stats{step}stats_page.html"
statsFile = f"{python_path}{step}stats{step}stats.json"
playerLogFile = f"{python_path}{step}playersData{step}profiles.json"
languageFile = f"{python_path}{step}data{step}language.json"

os.environ['BA_ACCESS_CHECK_VERBOSE'] = '1'
    
emptyData = {}
if not os.path.exists(playerLogFile):
    with open(playerLogFile, 'w') as f:
        f.write(json.dumps(emptyData))
        f.close()
if not os.path.exists(statsFile):
    with open(statsFile, 'w') as f:
        f.write(json.dumps(emptyData, indent=4))
        f.close()
if not os.path.exists(htmlFile):
    with open(htmlFile, 'w') as f:
        f.write(json.dumps(emptyData))
        f.close()   
if not os.path.exists(languageFile):
    with open(languageFile, 'w') as f:
        f.write(json.dumps(emptyData))
        f.close()        

def getStats():
    try:
        f = open(statsFile, 'r')
        return json.loads(f.read())
        f.close()
    except:
        sendError("Stats not found")
        return {}
        
multicolor = {0:((0+random.random()*3.0),(0+random.random()*3.0),(0+random.random()*3.0)),250:((0+random.random()*3.0),(0+random.random()*3.0),(0+random.random()*3.0)),500:((0+random.random()*3.0),(0+random.random()*3.0),(0+random.random()*3.0)),750:((0+random.random()*3.0),(0+random.random()*3.0),(0+random.random()*3.0)),1000:((0+random.random()*3.0),(0+random.random()*3.0),(0+random.random()*3.0)),1250:((0+random.random()*3.0),(0+random.random()*3.0),(0+random.random()*3.0)),1500:((0+random.random()*3.0),(0+random.random()*3.0),(0+random.random()*3.0)),1750:((0+random.random()*3.0),(0+random.random()*3.0),(0+random.random()*3.0)),2000:((0+random.random()*3.0),(0+random.random()*3.0),(0+random.random()*3.0)),2250:((0+random.random()*3.0),(0+random.random()*3.0),(0+random.random()*3.0)),2500:((0+random.random()*3.0),(0+random.random()*3.0),(0+random.random()*3.0))}

print('Scripts By : Sara :)')

