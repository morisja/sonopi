#!/usr/bin/python3
import os
import time
import sys
PLAYLISTS=["queen","ac/dc","bowie","robbie gill","turkuaz","the daily"]
ROWS=5
WIDTH=24
INITIAL_VOLUME=50
DEFAULT_TARGET="192.168.0.223"

class CommDriver:
    """Talk to the sonos controller service"""
    def __init__(self,target=DEFAULT_TARGET):
        pass
    def start_playlist(self,pl):
        print(f"start playlist {pl}")

    def play_pause(self):
        print(f"play/pause")
    def next(self):
        print(f"next")
    def prev(self):
        print(f"prev")

class ScreenDriver:
    """Consistently render the screen"""
    def __init__(self, rows=ROWS, cols=WIDTH):
        self.rmax=rows
        self.wmax=cols
        self.prefixes=["","","","",""]
        self.values=["","","","",""]

    def set_prefix(self,n,val):
        self.prefixes[n]=val

    def set_value(self,n,val):
        self.values[n]=val

    def render(self):
        for n in range(0,self.rmax):
            print(f"{self.prefixes[n]}{self.values[n]}")


class ScreenDefault:
    """The home screen for the app"""
    def __init__(self, sd:ScreenDriver ,cd=CommDriver, initial_volume=INITIAL_VOLUME,playing="Evening dinner",width=24):
        self.sd=sd
        self.cd=cd
        self.width=width
        self.max_vol=100
        self.vol=initial_volume
        self.playing=playing
        self.prefixes=["","Vol: ","Now: ","PL : ",""]
        self.values=["","","","",""]

    @property
    def vol_string(self):
        max_size = self.width - len(self.prefixes[0]) - 2
        chars = int((self.vol / 100) * max_size)
        n=0
        str=""
        while(n<max_size):
            if n<chars:
                str=str+"="
            else:
                str=str+" "
            n=n+1
        return f"[{str}]"

    @property
    def playing_string(self):
        return self.playing

    def scroll(self,inc):
        if (self.vol + inc) >= 0 and (self.vol + inc) <= self.max_vol:
            self.vol = self.vol + inc

    def scroll_select(self):
        pass

    def set_playing(self,new_playing):
        self.playing=new_playing

    def play_pause(self):
        self.cd.play_pause()
    def next(self):
        self.cd.next()
    def prev(self):
        self.cd.prev()

    def render(self):
        os.system('clear')
        self.values[1]=self.vol_string
        self.values[2]=self.playing_string
        for n,v in enumerate(self.prefixes):
            self.sd.set_prefix(n,v)
        for n,v in enumerate(self.values):
            self.sd.set_value(n,v)
        self.sd.render()

def test_default():
    sd=ScreenDriver()
    x=ScreenDefault(sd)
    x.render()

    for n in range(0,11):
        x.scroll(10)
        time.sleep(0.2)
        x.render()

    for s in ["ac/dc","bowie","turkuaz"]:
        x.set_playing(s)
        x.render()
        time.sleep(0.2)

    for n in range(0,11):
        x.scroll(-10)
        time.sleep(0.2)
        x.render()


class ScreenChooser:
    """Select from playlists"""
    def __init__(self, sd:ScreenDriver, cd:CommDriver, rmax=ROWS,all_playlists=PLAYLISTS):
        self.sd=sd
        self.cd=cd
        self.all_playlists=all_playlists
        self.rows=[]
        self.rmax=rmax
        self.pos=0
        self.prefixes=["---:","---:",">>>:","---:","---:"]

    
    def set_all_playlists(self,ap):
        self.all_playlists=ap

    def scroll(self,inc):
        if (self.pos + inc) >= 0 and (self.pos + inc) < len(self.all_playlists):
            self.pos = self.pos + inc

    def scroll_select(self):
        self.cd.start_playlist(self.selected)
        return self.selected

    @property
    def rowlist(self):
        rows=[]
        rows.extend(["",""])
        rows.extend(self.all_playlists)
        rows.extend(["",""])
        out= rows[self.pos:self.pos+self.rmax]
        self.selected=out[3]
        return out

    def render(self):
        os.system('clear')
        for n,v in enumerate(self.prefixes):
            self.sd.set_prefix(n,v)
        for n,v in enumerate(self.rowlist):
            self.sd.set_value(n,v)
        self.sd.render()

def test_screen_chooser():
    sd=ScreenDriver()
    cd=CommDriver()
    x=ScreenChooser(sd,cd)
    x.set_all_playlists(sorted(["queen","ac/dc","bowie","robbie gill","turkuaz","the daily"]))
    x.render()

    for n in range(0,10):
        time.sleep(0.3)
        x.scroll(1)
        x.render()

    for n in range(0,10):
        time.sleep(0.3)
        x.scroll(-1)
        x.render()

class App:
    """Control the app"""
    def __init__(self, screen_default:ScreenDefault, screen_chooser:ScreenChooser):
        self.sd=screen_default
        self.sc=screen_chooser
        self.current="default"
        self.ss = screen_default

    def scroll_action(self,inc):
        self.ss.scroll(inc)
        self.ss.render()

    def scroll_select(self):
        val=self.ss.scroll_select()
        if self.current=="default":
            self.current="chooser"
            self.ss=self.sc
        elif self.current=="chooser":
            self.current="default"
            self.ss=self.sd
            self.ss.set_playing(val)
        self.ss.render()

    def pp(self):
        self.sd.play_pause()
    def prev(self):
        self.sd.prev()
    def next(self):
        self.sd.next()
    def render(self):
        self.ss.render()

def test_app():
    sd=ScreenDriver()
    comm=CommDriver()
    x=App(ScreenDefault(sd,comm),ScreenChooser(sd,comm))
    x.render()
    while(1):
        action=input(":").lower()
        if action.startswith("l"):
            x.scroll_action(-1)
        if action.startswith("p"):
            x.scroll_action(1)
        if action.startswith("o"):
            x.scroll_select()
        if action.startswith("z"):
            x.pp()
        if action.startswith("x"):
            x.prev()
        if action.startswith("c"):
            x.next()
        if action.startswith("q"):
            sys.exit()

test_default()
time.sleep(1)
test_screen_chooser()
test_app()
sys.exit()

