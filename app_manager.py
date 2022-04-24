
from email.utils import parseaddr
from time import sleep
from soco import discover
from soco.plugins.sharelink import ShareLinkPlugin
import structlog
# initial state
import subprocess

logger = structlog.get_logger()

PLAYLISTS = [{
    "name":"Philly Soul",
    "link": "https://open.spotify.com/playlist/37i9dQZF1DWYmZJhCzQOPD"
},
{
    "name":"Classic Acoustic",
    "link":"https://open.spotify.com/playlist/37i9dQZF1DX504r1DvyvxG"
},{
    "name": "Greta",
    "link": "https://open.spotify.com/playlist/7yF49cwKHcWXbn0Xi504Yk"
}]

DEFAULT_DEVICE_NAME="Living Room"

class ExecFailure(Exception):
    pass

class AppManager():
    def __init__(self, default_device, playlists = PLAYLISTS, playlist_pos=0):
        self.sonos_bin="/home/pi/.local/bin/sonos"
        self.default_device = default_device
        self.playlists = playlists
        self.playlist_pos=playlist_pos

    def _exec_cmd(self,cmd):
        print(cmd)
        ret = subprocess.run(cmd, capture_output=True)
        if ret.returncode != 0:
            raise ExecFailure()
        print(ret)
        s = ret.stdout.decode().rstrip()
        return s
    def _exec_sonos(self,args):
        return self._exec_cmd([self.sonos_bin] + args)
    def _native_pause(self):
        self.default_device.pause()
    def _native_play(self):
        self.default_device.play()
    def _native_play_uri(self):
        name = self.playlists[self.playlist_pos]["name"]
        link = self.playlists[self.playlist_pos]["link"]
        share_link = ShareLinkPlugin(self.default_device)
        logger.info(f"Playing {name} {link} on {self.default_device.player_name}")
        index=share_link.add_share_link_to_queue(link)
        self.default_device.play_from_queue(index, start=True)
    def pause(self):
        self._exec_sonos(["Living Room", "pause"])
    def play(self):
        self._exec_sonos(["Living Room", "play"])
    def set_playlist(self):
        pos=self._exec_sonos(["Living Room", "sharelink", self.playlists[self.playlist_pos]["link"]])
        play_next=int(pos)
        sleep(0.1)
        pos=self._exec_sonos(["Living Room", "play_from_queue", str(play_next)])
    def scroll_left(self):
        if self.playlist_pos > 0:
            self.playlist_pos = self.playlist_pos -1
            print(self.playlists[self.playlist_pos]["name"])
    def scroll_right(self):
        if self.playlist_pos < len(self.playlists) -1:
            self.playlist_pos = self.playlist_pos +1
            print(self.playlists[self.playlist_pos]["name"])
    def press_select(self):
        self._native_play_uri()
    def press_k1(self):
        logger.info("pause")
        self._native_pause()
    def press_k2(self):
        logger.info("play")
        self._native_play()

def get_app_manager():
    sonos_devices=discover()
    for s in sonos_devices:
        if s.player_name == DEFAULT_DEVICE_NAME:
            d=s
    return AppManager(default_device=d)