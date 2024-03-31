#Maded by Froshlee14
import bs,random, bsSpaz,bsBomb,bsUtils, bsInternal,bsMainMenu,bsPowerup
from bsSpaz import _PunchHitMessage,_PickupMessage

def bsGetAPIVersion():
    return 4

def bsGetGames():
    return [BotsVsBots]
	
def bsGetLevels():
    return [bs.Level('Bots vs Bots', displayName='${GAME}',gameType=BotsVsBots,previewTexName='rampagePreview',settings={})]

	
class MelBot(bsSpaz.SpazBot):
    character = 'Mel'
    punchiness = 0.9
    throwiness = 0.1
    run = True
    chargeDistMin = 4.0
    chargeDistMax = 10.0
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 0.0
    throwDistMax = 4.0
    throwRate = 2.0
    defaultBombType = 'sticky'
    defaultBombCount = 1
		
class FroshBot(bsSpaz.SpazBot):
    color=(0.13,0.13,0.13)
    highlight=(0.2,1,1)
    character = 'Bernard'
    run = True
    throwiness = 0.2
    punchiness = 0.9
    chargeDistMax = 1.0
    chargeSpeedMin = 0.3
    chargeSpeedMax = 1.0
	
class RobotBot(bsSpaz.ToughGuyBot):
    color=(0.5,0.5,0.5)
    highlight=(0,10,0)
    character = 'B-9000'
    chargeSpeedMin = 0.3
    chargeSpeedMax = 1.0

    def handleMessage(self,m):

        super(self.__class__, self).handleMessage(m)
        def _safeSetAttr(node,attr,val):
            if node.exists(): setattr(node,attr,val)
        bs.gameTimer(500,bs.Call(_safeSetAttr,self.node,'hockey',True))

class PascalBot(bsSpaz.SpazBot):
    color=(0,0,3)
    highlight=(0.2,0.2,1)
    character = 'Pascal'
    bouncy = True
    run = True
    punchiness = 0.8
    throwiness = 0.1
    chargeSpeedMin = 0.5
    chargeSpeedMax = 0.8

    def handleMessage(self,m):
        if isinstance(m, _PunchHitMessage):
            node = bs.getCollisionInfo("opposingNode")
            try:
                node.handleMessage(bs.FreezeMessage())
                bs.playSound(bs.getSound('freeze'))
            except Exception: print('Cant freeze')
            super(self.__class__, self).handleMessage(m)
        elif isinstance(m, bs.FreezeMessage):pass
        else: super(self.__class__, self).handleMessage(m)
	
class NewBotSet(bsSpaz.BotSet):
    def _update(self):
        try:
            botList = self._botLists[self._botUpdateList] = [b for b in self._botLists[self._botUpdateList] if b.exists()]
        except Exception:
            bs.printException("error updating bot list: "+str(self._botLists[self._botUpdateList]))
        self._botUpdateList = (self._botUpdateList+1)%self._botListCount
        playerPts = []
        for n in bs.getNodes():
                if n.getNodeType() == 'spaz':
                    s = n.getDelegate()
                    if isinstance(s,bsSpaz.PlayerSpaz):
                        if s.isAlive():
                            playerPts.append((bs.Vector(*n.position), bs.Vector(*n.velocity)))
                    if isinstance(s,bsSpaz.SpazBot):
                        if not s in self.getLivingBots():
                            playerPts.append((bs.Vector(*n.position), bs.Vector(*n.velocity)))

        for b in botList:
            b._setPlayerPts(playerPts)
            b._updateAI()

class BotsVsBots(bs.TeamGameActivity):

    @classmethod
    def getName(cls):
        return 'Bots vs Bots'
    
    @classmethod
    def getDescription(cls,sessionType):
        return 'Enjoy the battle.'

    @classmethod
    def getSupportedMaps(cls,sessionType):
        return ['Football Stadium']

    @classmethod
    def getSettings(cls,sessionType):
        return [("Epic Mode",{'default':False}),
                       ("Bots per Team",{'minValue':5,'maxValue':20,'default':6,'increment':1})]
    
    @classmethod
    def supportsSessionType(cls,sessionType):
        return True if (issubclass(sessionType,bs.TeamsSession)
                        or issubclass(sessionType,bs.FreeForAllSession)
                        or issubclass(sessionType,bs.CoopSession)) else False

    def __init__(self,settings):
        bs.TeamGameActivity.__init__(self,settings)
        if self.settings['Epic Mode']: self._isSlowMotion = True
        
    def onTransitionIn(self):
        bs.TeamGameActivity.onTransitionIn(self, music='Epic' if self.settings['Epic Mode'] else 'Survival')

    def onBegin(self):
        bs.TeamGameActivity.onBegin(self)
        self._bots = NewBotSet()
        self._bots2 = NewBotSet()
		
        self._hasEnded = False

        for i in range(self.settings['Bots per Team']):
            bPos = (-12,1.5,random.randrange(-4,5))
            bs.gameTimer(0,bs.Call(self._bots.spawnBot,self._getRandomBotType(),pos=bPos,spawnTime=4000,onSpawnCall=bs.Call(self.setRedTeam)))
            bPos = (12,1.5,random.randrange(-4,5))
            bs.gameTimer(0,bs.Call(self._bots2.spawnBot,self._getRandomBotType(),pos=bPos,spawnTime=4000,onSpawnCall=bs.Call(self.setBlueTeam)))
		
    def setRedTeam(self,spaz):
        spaz.node.color = (1,0,0)

    def setBlueTeam(self,spaz):
        spaz.node.color = (0,0,1)
		
    def _getRandomBotType(self):
        bt = [bs.ToughGuyBot,
              bs.NinjaBot,
              bs.BunnyBot,
              PascalBot,
              MelBot,
              RobotBot,
              FroshBot,]
        return (random.choice(bt))
               
    def spawnPlayer(self,player):
        return
 
    def handleMessage(self,m):
        if isinstance(m,bs.SpazBotDeathMessage):
            bs.pushCall(self._checkEndGame)
            bs.TeamGameActivity.handleMessage(self,m) 
        else:
            bs.TeamGameActivity.handleMessage(self,m)
			
    def _checkEndGame(self):
        if self._hasEnded: return
        if len(self._bots.getLivingBots()) == 0:
            self.endGame(winners=' Blue',color=(0,0,1))
            self._hasEnded = True
        elif len(self._bots2.getLivingBots()) == 0:
            self.endGame(winners=' Red',color=(1,0,0))
            self._hasEnded = True
			
    def showZoomMessage(self,message,color=(0.9,0.4,0.0),position=None,scale=0.8,duration=2000,trail=False):
        try: times = self._zoomMessageTimes
        except Exception: self._zoomMessageTimes = {}
        i = 0
        curTime = bs.getGameTime()
        while True:
            if i not in self._zoomMessageTimes or self._zoomMessageTimes[i] < curTime:
                self._zoomMessageTimes[i] = curTime + duration
                break
            i += 1
        if position == None: position = (0,200-i*100)
        bsUtils.ZoomText(message,lifespan=duration,jitter=2.0,position=position,scale=scale,maxWidth=800, trail=trail,color=color).autoRetain()
			
    def endGame(self,winners=None,color=(1,1,1)):
        msg = (str(winners) + ' team win')
        self.showZoomMessage(msg,scale=1.0,duration=3000,trail=True,color=color)
        self.cameraFlash()
        bs.gameTimer(3000,self.fadeEnd)
		
    def fadeEnd(self):
        def callback():
            bsInternal._unlockAllInput()
            bsInternal._newHostSession(bsMainMenu.MainMenuSession)
        bsInternal._fadeScreen(False, time=500, endCall=callback)
        bsInternal._lockAllInput()