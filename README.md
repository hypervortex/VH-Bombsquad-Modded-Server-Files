# 𝙑𝙃~𝘽𝙤𝙢𝙗𝙨𝙦𝙪𝙖𝙙-𝙎𝙚𝙧𝙫𝙚𝙧-𝙁𝙞𝙡𝙚𝙨-1.7(𝘽𝘾𝙎-𝙈𝙤𝙙𝙞𝙛𝙞𝙚𝙙)

Special Thanks to sara and [PCModder]([https://github.com/mikahael)..!

All rights reserved [vortex1555]([https://github.com/hypervortex]) as the license states.

Basic knowledge of Linux
A VPS (e.g. Amazon Web Services, Microsoft Azure)
Any Linux distribution.
It is recommended to use Ubuntu.
Python 3.10.12
1 GB free Memory (Recommended 2 GB)

Getting Started

Requires UBUNTU 22.04

Requires PYTHON 3.10.12

## Download server files.
- sudo git clone https://github.com/hypervortex/Bombsuqad-Modded-Server-Files.git

## 𝙄𝙣𝙨𝙩𝙖𝙡𝙡𝙖𝙩𝙞𝙤𝙣 𝙋𝙧𝙤𝙘𝙚𝙨𝙨 - 𝘼𝙪𝙩𝙤𝙢𝙖𝙩𝙞𝙘 𝙄𝙣𝙨𝙩𝙖𝙡𝙡𝙖𝙩𝙞𝙤𝙣:

```
chmod 777 bs_requirements.sh
```
sudo ./bs_requirements.sh
```

Required packages downloaded, for manual installation see below
Now you can edit rest files

## 𝙈𝙖𝙣𝙪𝙖𝙡 𝙄𝙣𝙨𝙩𝙖𝙡𝙡𝙖𝙩𝙞𝙤𝙣:
- Open terminal, run the followng commands:

  - sudo apt update; sudo apt install software-properties-common -y
  - sudo add-apt-repository ppa:deadsnakes/ppa
  - sudo apt install python3-pip python3.10-dev python3.10-venv
  - install the pymongo and psutil
  - sudo apt install python3-pip -y
  - pip3 install pymongo --target=/usr/lib/python3.10
  - pip3 install psutil --target=/usr/lib/python3.10


## 𝘾𝙧𝙚𝙖𝙩𝙚 𝙖 𝙏𝙈𝙐𝙓 𝙨𝙚𝙨𝙨𝙞𝙤𝙣:
- How to run server:

  - tmux new -s 43210
  - cd (Your_folder_name)
  - edit config.yaml ---> change server name, team names, team colors, etc
  - chmod 777 bombsquad_server
  - chmod 777 dist/bombsquad_headless
  - start the server - sudo ./bombsquad_server
  - More Configurations  --->
  - Open dist/ba_root/mods/setting.json in your prefered editor and change values according to you.
  - Knowledge of BCS files and basic editing senses is expected.

# 𝙁𝙚𝙖𝙩𝙪𝙧𝙚𝙨
Includes latest BCS-Server features and special features by me - vortex1555

### 𝙎𝙥𝙚𝙘𝙞𝙖𝙡 𝙑𝙊𝙍𝙏𝙀𝙓 𝘾𝙈𝘿𝙎 𝙗𝙮 𝙈𝙚:
- zoommessage (zm),
- fall,
- speedon,
- hug,
- icy,
- spaz,
- top,
- setscore,
- zombieall,
- boxall,
- texall,
- kickall,
- ooh,
- spazall,
- acl (admin cmd list) ,
- vcl ( vip cmd list ) ,
- tint,
- ac,
- comp ( to file complaint agaist player, but u need to setup dc bot to use this cmd),
- rainbow,
- Playsound
 * Time and member count in textonmap 
 * Modified season reset count down which is fully visible

# 𝘾𝙤𝙞𝙣𝙨𝙮𝙨𝙩𝙚𝙢 - 𝙎𝙥𝙚𝙘𝙞𝙖𝙡 𝙑𝙃 𝙁𝙚𝙖𝙩𝙪𝙧𝙚:

1.Added a coins/tickets system and shop. Players can buy effects and tags with tickets. You can modify the expiry time of purchases. There's also a command to remove paid effects (/rpe 113) so players can correct their purchases.

2.Introducing Daily Claim:
Well, you can turn off questions and use the daily claim feature, so people can't use the auto-answer plugin, engaging players more to play daily.

# 𝘿𝙞𝙨𝙘𝙤𝙧𝙙 𝘽𝙤𝙩:

## 𝘾𝙤𝙤𝙡 𝙈𝙤𝙙𝙞𝙛𝙞𝙚𝙙 𝙎𝙩𝙖𝙩𝙨 𝙐𝙄
### ![image](https://github.com/hypervortex/Bombsuqad-Modded-Server-Files/assets/75498823/250b1511-627d-44ab-b397-98077c27246b)

* You can easily add admin, VIP, owner, custom tags, effects, staff, and mods directly from your Discord server.
* Efficient Server Management using Discord commands. You can do everything from Discord, like adding effects, muting, tags, roles, restarting server, getting player info such as rank, * * * score, device id, IP, and many more data. To get more details, set up the bot and try v!help.
* Advanced banning system using MongoDB. If you are hosting multiple servers, then it's a very useful feature for you. Just ban once, and it will get banned in all servers, and even if you * lose server files data, your banlist is still safe.
* Added a complaint feature from the game to Discord, so people don't need to leave the game to complain on Discord.
* Added Notify feature. If you used BCS manager, then you may know about the feature regarding subscribed players. You get notified when that subscribed player joins the server, so this is * the same feature but notifies in the Discord server. You just need to add another channel id and role to ping, so you will get notified.
* Player Data Check: Easily check player ranks and see the top 10 players on your servers.
* Bot security: Added security to ensure only authorized members and servers can execute commands.
* Enhanced Custom Effects: Modified existing effects such as fairydust and sweat and added more beardmods(1.8) effects.
* Added autoadmin along with the score. So rank 1, 2, 3 with specified score will get admin and VIPs.
* Check setting json for more settings. You can set up your bot prefix as you want.

# 𝙏𝙊 𝙒𝙃𝙊𝙈𝙎𝙊𝙀𝙑𝙀𝙍 𝙄𝙏 𝙈𝘼𝙔 𝘾𝙊𝙉𝘾𝙀𝙍𝙉:

𝘼𝙡𝙡 𝙧𝙞𝙜𝙝𝙩𝙨 𝙩𝙤 𝙑𝙤𝙧𝙩𝙚𝙭 𝙖𝙨 𝙩𝙝𝙚 𝙇𝙞𝙘𝙚𝙣𝙨𝙚 𝙨𝙩𝙖𝙩𝙚𝙨 𝙖𝙗𝙤𝙫𝙚

𝘾𝙧𝙚𝙖𝙩𝙚𝙙 𝙗𝙮 𝙑𝙊𝙍𝙏𝙀𝙓1555

𝙎𝙥𝙚𝙘𝙞𝙖𝙡 𝙩𝙝𝙖𝙣𝙠𝙨 𝙩𝙤 𝙋𝘾𝙈𝙊𝘿𝘿𝙀𝙍 𝙖𝙣𝙙 𝙎𝘼𝙍𝘼


#To whom ever this may concern, All rights to VORTEX aka vortex1555 as the License states above.

![VORTEx(1)](https://github.com/hypervortex/Bombsuqad-Modded-Server-Files/assets/54455412/d726cb33-a900-420c-81e5-8e168a3967b4)


