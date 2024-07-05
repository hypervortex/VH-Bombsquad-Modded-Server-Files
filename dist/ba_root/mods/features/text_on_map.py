# Released under the MIT License. See LICENSE for details.

""" TODO need to set coordinates of text node , move timer values to settings.json """

from ba._generated.enums import TimeType
import ba, _ba
import ba.internal
import setting
from stats import mystats
from datetime import date, datetime
from features import map
import pytz
import random
import members.members as mid     
counts = mid.members
size = len(counts)   
setti=setting.get_settings_data()
time_str = map.update_season_info()

class textonmap:

    def __init__(self):
        data = setti['textonmap']
        left = data['bottom left watermark']
        top = data['top watermark']
        nextMap=""
        try:
            nextMap=ba.internal.get_foreground_host_session().get_next_game_description().evaluate()
        except:
            pass
        top = top.replace("@IP", _ba.our_ip).replace("@PORT", str(_ba.our_port))
        self.index = 0
        self.highlights = data['center highlights']["msg"]
        self.left_watermark(left)
        self.top_message(top)
        self.nextGame(nextMap)
        self.restart_msg()
        self.season_reset()
        self.timer = ba.timer(0.1, ba.Call(self.season_reset), repeat=True)
        if setti["leaderboard"]["enable"]:
            self.leaderBoard()
        if setti["textonmap"]['center highlights']["enable"]:
            self.highlights_()
            self.timer = ba.timer(8.0, ba.Call(self.highlights_), repeat=True)
        if setti["timetext"]["enable"]:
            self.show_date_time()
            self.timer = ba.timer(0.1, ba.Call(self.show_date_time), repeat = True)
        if setti["TopMapText"]["enable"]:
            self.show_top_text()
            self.timer = ba.timer(5.0, ba.Call(self.show_top_text), repeat = True)     
        
    def highlights_(self):
        if setti["textonmap"]['center highlights']["randomColor"]:
            color=((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))
        else:
            color=tuple(setti["textonmap"]["center highlights"]["color"])
        node = _ba.newnode('text',
                            attrs={
                                'text': self.highlights[self.index],
                                'flatness': 1.0,
                                'h_align': 'center',
                                'v_attach':'bottom',
                                'scale':1,
                                'position':(0,138),
                                'color':(1,1,1)})
        ba.animate_array(
             node,
             "color",
             3,
             {
                  0: (1,0,0),
                  0.2: (1,0.5,0),
                  0.4: (1,1,0),
                  0.6: (0,1,0),
                  0.8: (0,1,1),
                  1.0: (1,0,1),
                  1.2: (1,0,0),
             },
             loop=True,
       )    
        self.delt = ba.timer(8.0,node.delete),
        ba.animate(node,'scale', {0.0: 0, 0.2: 1, 7.8: 1, 8.0: 0})
        self.index = int((self.index+1)%len(self.highlights))


    def show_date_time(self):
          time = setti["timetext"]["timezone"]
          node = _ba.newnode('text',
                          attrs={
                              'text': u"" + "Date : " + str(datetime.now(pytz.timezone(time)).strftime("%A, %B %d, %Y")) + "\nTime : " + str(datetime.now(pytz.timezone(time)).strftime("%I:%M:%S %p")),
                              'scale': 0.85,
                              'flatness': 1,
                              'maxwidth': 0,
                              'h_attach': 'center',
                              'h_align': 'center',
                              'v_attach':'top',
                              'position':(400,-60),
                              'color':(1,1,1)})
          self.delt = ba.timer(0.1, node.delete)   

    def show_top_text(self):
        texts = setti["TopMapText"]["msg"]
        node = _ba.newnode('text',
                    attrs={
                        'text': random.choice(texts),
                        'flatness': 3.0,
                        'h_align': 'center',
                        'v_attach':'top',
                        'scale':1.2,
                        'position':(0,-55),
                        'color':(1,1,1)})      
        ba.animate_array(
             node,
             "color",
             3,
             {
                  0: (1,0,0), 
                  1.2: (0,1,0), 
                  2: (0,0,1), 
                  3.1: (1,0,0),
             },
             loop=True,
       )      
        ba.animate(node,'opacity', {0.0: 0, 1.0: 2, 4.0: 2, 5.0: 0})
        self.delt = ba.timer(5.0, node.delete)       

    def left_watermark(self, text):
        node = _ba.newnode('text',
                            attrs={
                                'text': text,
                                'flatness': 1.0,
                                'h_align': 'left',
                                'v_attach':'bottom',
                                'h_attach':'left',
                                'scale':0.7,
                                'position':(25,95),
                                'color':(1,1,1)})
        ba.animate_array(
             node,
             "color",
             3,
             {
                  0: (1,0,0),
                  0.2: (1,0.5,0),
                  0.4: (1,1,0),
                  0.6: (0,1,0),
                  0.8: (0,1,1),
                  1.0: (1,0,1),
                  1.2: (1,0,0),
             },
             loop=True,
       )   
        node = _ba.newnode('text',
                            attrs={
                                'text':u'\ue043[\U0001F451] OWNER : VORTEX & HONOR\n\ue048[\U0001F6E0] MANAGED BY : TEAM VORTEX',
                                'flatness': 1.0,
                                'h_align': 'left',
                                'v_attach':'bottom',
                                'h_attach':'left',
                                'scale':0.7,
                                'position':(25,40),
                                'color':(1,1,1)
                            }) 

    def nextGame(self,text):
        node = _ba.newnode('text',
                            attrs={
                                'text':"Next : "+text               ,
                                'flatness':0.4,
                                'h_align':'right',
                                'v_attach':'bottom',
                                'h_attach':'right',
                                'scale':0.7,
                                'position':(-25,5),
                                'color':(1,1,1)
                            })

    def season_reset(self):
        text = time_str()
        node = _ba.newnode('text',
                            attrs={
                                'text':text,
                                'flatness':1.0,
                                'h_align':'right',
                                'v_attach':'bottom',
                                'h_attach':'right',
                                'scale':0.7,
                                'position':(-25, 25),
                                'color':(1,1,1)
                            })
        self.delt = ba.timer(0.1, node.delete)   


    def restart_msg(self):
        if hasattr(_ba,'restart_scheduled'):
            _ba.get_foreground_host_activity().restart_msg = _ba.newnode('text',
                                attrs={
                                    'text':"Server going to restart after this series.",
                                    'flatness':1.0,
                                    'h_align':'right',
                                    'v_attach':'bottom',
                                    'h_attach':'right',
                                    'scale':0.3,
                                    'position':(-25,40),
                                    'color':(1,0.5,0.7)
                                })

    def top_message(self, text):
        node = _ba.newnode('text',
                            attrs={
                                'text': text,
                                'flatness': 1.0,
                                'h_align': 'center',
                                'v_attach':'top',
                                'scale':1.2,
                                'position':(0,-70),
                                'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))
                            })

        node = _ba.newnode('text',
                            attrs={
                                'text':u'',
                                'flatness': 3.0,
                                'h_align': 'center',
                                'v_attach':'top',
                                'scale':2.0,
                                'position':(0,-67),
                                'color':(1,1,1)})       
        ba.animate_array(
             node,
             "color",
             3,
             {
                  0: (1,0,0), 
                  1.2: (0,1,0), 
                  2: (0,0,1), 
                  3.1: (1,0,0),
             },
             loop=True,
       )      
        ba.animate(node,'opacity', {0.0: 2.0, 2.0: 1.8, 4.0: 2.0, 6.0: 1.8, 8.0: 2.0, 10.0: 1.5, 12.0: 2.0, 14.0: 1.8, 16.0: 2.0, 18.0: 1.8, 20.0: 2.0, 22.0: 1.5, 24.0: 2.0, 26.0: 1.8, 28.0: 2.0, 30.0: 1.8, 32.0: 2.0, 34.0: 2.0, 36.0: 1.8, 38.0: 2.0, 40.0: 1.8, 42.0: 2.0, 44.0: 1.5, 46.0: 2.0, 48.0: 1.8, 50.0: 2.0, 52.0: 1.8, 54.0: 2.0, 56.0: 1.5, 58.0: 2.0, 60.0: 1.8, 62.0: 2.0, 64.0: 1.8, 66.0: 2.0})

        node = _ba.newnode('text',
                            attrs={
                                'text':u'\ue048CONTACT OWNER FOR DETAILS & SUGGESTION\ue048\n\ue00cHAPPY BOMBSQUADING\ue00c',
                                'flatness': 3.0,
                                'h_align': 'center',
                                'v_attach':'top',
                                'scale':0.5,
                                'position':(0,-75),
                                'color':(1,1,1)
                             })

        node = _ba.newnode('text',
                            attrs={
                                'text':u'\ue043Join Discord Server From Stats Button\ue043',
                                'flatness': 0.4,
                                'h_align': 'center',
                                'v_attach':'bottom',
                                'scale':0.7,
                                'position':(0,0),
                                'color':(1,1,1)})     
        ba.animate_array(
             node,
             "color",
             3,
             {
                  0: (1,0,0), 
                  3: (0,1,0), 
                  6: (0,0,1), 
                  9: (1,0,0),
             },
             loop=True,
        )
           
        count = ("\n\n\ue043| MEMBERS COUNT: "+str(size)+" |\ue043")
        node = _ba.newnode('text',
                    attrs={
                        'text': count,
                        'scale': 0.75,
                        'flatness': 1,
                        'maxwidth': 0,
                        'h_attach': 'center',
                        'h_align': 'center',
                        'v_attach':'top',
                        'position':(400,-62),
                        'color':(1,1,1)})      
        ba.animate_array(
             node,
             "color",
             3,
             {
                  0: (1, 0, 0),
                  0.2: (1, 0.5, 0),
                  0.6: (1,1,0),
                  0.8: (0,1,0),
                  1.0: (0,1,1),
                  1.4: (1,0,1),
                  1.8: (1,0,0),
             },
             loop=True,
        )            
        node = _ba.newnode('text',
                            attrs={
                                'text':u'\ue048| VH PARADISE |\ue048',
                                'flatness':1.0,
                                'h_align':'center',
                                'v_attach':'top',
                                'h_attach':'center',
                                'scale':0.75,
                                'position':(400,-35),
                                'color':(1,1,1)})
        ba.animate_array(
             node,
             "color",
             3,
             {
                  0: (1,0,0),
                  0.2: (1,0.5,0),
                  0.4: (1,1,0),
                  0.6: (0,1,0),
                  0.8: (0,1,1),
                  1.0: (1,0,1),
                  1.2: (1,0,0),
             },
             loop=True,
       )

    def leaderBoard(self):
        if len(mystats.top5Name) >2:
            if setti["leaderboard"]["barsBehindName"]:
                self.ss1=ba.newnode('image',attrs={'scale':(300,30),'texture':ba.gettexture('bar'),'position':(0,-80),'attach':'topRight','opacity':0.5,'color':(0.7,0.1,0)})
                self.ss1=ba.newnode('image',attrs={'scale':(300,30),'texture':ba.gettexture('bar'),'position':(0,-115),'attach':'topRight','opacity':0.5,'color':(0.6,0.6,0.6)})
                self.ss1=ba.newnode('image',attrs={'scale':(300,30),'texture':ba.gettexture('bar'),'position':(0,-150),'attach':'topRight','opacity':0.5,'color':(0.1,0.3,0.1)})

            self.ss1a=ba.newnode('text',attrs={'text':"#\U0001F947 "+mystats.top5Name[0][:10]+"...",'flatness':1.0,'h_align':'left','h_attach':'right','v_attach':'top','v_align':'center','position':(-140,-80),'scale':0.7,'color':(0.7,0.4,0.3)})

            self.ss1a=ba.newnode('text',attrs={'text':"#\U0001F948 "+mystats.top5Name[1][:10]+"...",'flatness':1.0,'h_align':'left','h_attach':'right','v_attach':'top','v_align':'center','position':(-140,-115),'scale':0.7,'color':(0.8,0.8,0.8)})

            self.ss1a=ba.newnode('text',attrs={'text':"#\U0001F949 "+mystats.top5Name[2][:10]+"...",'flatness':1.0,'h_align':'left','h_attach':'right','v_attach':'top','v_align':'center','position':(-140,-150),'scale':0.7,'color':(0.2,0.6,0.2)})
