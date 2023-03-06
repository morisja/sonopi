from time import sleep
from soco import discover
from soco.plugins.sharelink import ShareLinkPlugin
from dataclasses import dataclass, asdict
from typing import Optional, List
import zlib
import hashlib
import structlog
import logging
import json


logger = structlog.get_logger()
DEFAULT_DEVICE_NAME = "Living Room"

@dataclass
class PlaylistItem:
    name: str
    link: str
    id: Optional[str] = None

    def __post_init__(self):
        self.id=hashlib.md5(self.name.encode('utf-8')).hexdigest()


#todo add id
PLAYLISTS = sorted([
    PlaylistItem(**i) for i in 
    [
        {
            "name": "Philly Soul",
            "link": "https://open.spotify.com/playlist/37i9dQZF1DWYmZJhCzQOPD",
        },
        {
            "name": "Classic Acoustic",
            "link": "https://open.spotify.com/playlist/37i9dQZF1DX504r1DvyvxG",
        },
        {
            "name": "Greta",
            "link": "https://open.spotify.com/playlist/7yF49cwKHcWXbn0Xi504Yk",
        },
        {
            "name": "Blues and Roots",
            "link": "https://open.spotify.com/playlist/37i9dQZF1DWSKpvyAAcaNZ",
        },
        {
            "name": "Gamble & Huff",
            "link": "https://open.spotify.com/playlist/37i9dQZF1DWXutrsZUdv7b",
        },
        {
            "name": "Evening dinner with lover and friends",
            "link": "https://open.spotify.com/playlist/4lnT8VECXVdwunurpgwyKL",
        },
        {
            "name": "Stoner Rock",
            "link": "https://open.spotify.com/playlist/2zwum1G8rCaRYCQ1blWflb",
        },
        {
            "name": "The Daily",
            "link": "https://open.spotify.com/show/3IM0lmZxpFAY7CwMuv9H4g",
        },
    ]
], key=lambda i:i.name)

class SonosManager:
    def __init__(
        self,
        play_status,
        volume: int,
        default_device,
        mode="CONTROL",
        playlists:List[PlaylistItem] = PLAYLISTS,
        playlist_pos: int = 0,
    ):
        self.default_device = default_device
        self.playlists = playlists
        self.playlist_pos = playlist_pos
        self.play_status = play_status
        self.volume = volume
        self.mode = mode

    def _native_pause(self):
        logger.info("pause")
        self.default_device.pause()

    def _native_play(self):
        logger.info("play")
        self.default_device.play()

    def _native_next(self):
        logger.info("next")
        self.default_device.next()

    def _native_previous(self):
        logger.info("previous")
        self.default_device.previous()

    def _native_play_by_uri(self, pl: PlaylistItem):
        name = pl.name
        link = pl.link
        share_link = ShareLinkPlugin(self.default_device)
        logger.info(f"Playing {name} {link} on {self.default_device.player_name}")
        self.default_device.clear_queue()
        index = share_link.add_share_link_to_queue(link)
        logger.info(f"index {index}")
        self.default_device.play_from_queue(index, start=True)

        self.play_status = self.default_device.get_current_transport_info()[
            "current_transport_state"
        ]

    def _native_get_info(self):
        dat={}
        t = self.default_device.get_current_track_info()
        logger.info(f"track - {t['artist']} - {t['title']} - {t['position']}")
        dat["artist"] = t["artist"]
        dat["title"] = t["title"]
        t = self.default_device.get_current_transport_info()
        logger.info(f"status - {t['current_transport_status']} {t['current_transport_state']}")
        dat["status"]=t['current_transport_status']
        dat["state"]=t['current_transport_state']
        return dat

    def _native_toggle_play_pause(self):
        if self.play_status == "PLAYING":
            self.default_device.pause()
            self.play_status = "PAUSED_PLAYBACK"
        elif self.play_status == "PAUSED_PLAYBACK":
            self.default_device.play()
            self.play_status = "PLAYING"
        elif self.play_status == "TRANSITIONING":
            self.play_status = self.default_device.get_current_transport_info()[
                "current_transport_state"
            ]
        else:
            self.default_device.play()
            self.play_status = "PLAYING"
        logger.info(f"{self.play_status}")

    def _native_toggle_mode(self):
        if self.mode == "CONTROL":
            self.mode = "VOLUME"
        else:
            self.mode = "CONTROL"
        logger.info(f"{self.mode}")


    def manage_volume(self, n: int):
        new_vol = self.volume + n
        if new_vol < 0:
            new_vol = 0
        if new_vol > 100:
            new_vol = 100
        self.default_device.volume = new_vol
        if n > 0:
            action="up"
        else:
            action="down"
        self.volume = new_vol
        logger.info(f"vol = {self.volume} {action}")

    def select(self, id: str):
        pl=next(p for p in self.playlists if p.id==id)
        self._native_play_by_uri(pl)

    def vol_up(self,n: int):
        return self.manage_volume(n)

    def vol_down(self,n: int):
        return self.manage_volume(n)
    def play_pause(self):
        return self._native_toggle_play_pause()
        
    def next(self):
        return self._native_next()
    def previous(self):
        return self._native_previous()
    def info(self):
        return self._native_get_info()

    def get_playlists(self):
        out=[]
        for i in self.playlists:
            out.append(asdict(i))
        return out

    def scroll_left(self):
        if self.mode == "CONTROL":
            if self.playlist_pos > 0:
                self.playlist_pos = self.playlist_pos - 1
                print(self.playlists[self.playlist_pos].name)
        if self.mode == "VOLUME":
            print(x._volume())
            self.manage_volume(-3)

    def scroll_right(self):
        if self.mode == "CONTROL":
            if self.playlist_pos < len(self.playlists) - 1:
                self.playlist_pos = self.playlist_pos + 1
                print(self.playlists[self.playlist_pos]["name"])
        if self.mode == "VOLUME":
            self.manage_volume(3)
        

def get_sonos_manager() -> SonosManager:
    sonos_devices = discover()
    for s in sonos_devices:
        if s.player_name == DEFAULT_DEVICE_NAME:
            d = s
    return SonosManager(
        d.get_current_transport_info()["current_transport_state"],
        d.volume,
        default_device=d,
    )
