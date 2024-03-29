from time import sleep
from soco import discover
from soco.plugins.sharelink import ShareLinkPlugin
import structlog
import logging
import json


logger = structlog.get_logger()

PLAYLISTS = sorted(
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
    ],
    key=lambda i: (i["name"]),
)

DEFAULT_DEVICE_NAME = "Living Room"
class AppManager:
    def __init__(
        self,
        play_status,
        volume: int,
        default_device,
        mode="CONTROL",
        playlists=PLAYLISTS,
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

    def _native_play_uri(self):
        name = self.playlists[self.playlist_pos]["name"]
        link = self.playlists[self.playlist_pos]["link"]
        share_link = ShareLinkPlugin(self.default_device)
        logger.info(f"Playing {name} {link} on {self.default_device.player_name}")
        index = share_link.add_share_link_to_queue(link)
        self.default_device.play_from_queue(index, start=True)

        self.play_status = self.default_device.get_current_transport_info()[
            "current_transport_state"
        ]

    def _native_get_info(self):
        t = self.default_device.get_current_track_info()
        logger.info(f"track - {t['artist']} - {t['title']} - {t['position']}")
        t = self.default_device.get_current_transport_info()
        logger.info(f"status - {t['current_transport_status']} {t['current_transport_state']}")

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

    def info(self):
        self._native_get_info()

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

    def scroll_left(self):
        if self.mode == "CONTROL":
            if self.playlist_pos > 0:
                self.playlist_pos = self.playlist_pos - 1
                print(self.playlists[self.playlist_pos]["name"])
        if selfprint(x._volume()).mode == "VOLUME":
            self.manage_volume(-3)

    def scroll_right(self):
        if self.mode == "CONTROL":
            if self.playlist_pos < len(self.playlists) - 1:
                self.playlist_pos = self.playlist_pos + 1
                print(self.playlists[self.playlist_pos]["name"])
        if self.mode == "VOLUME":
            self.manage_volume(3)

    def press_select(self):
        self._native_play_uri()

    def press_k1(self):
        self._native_toggle_play_pause()

    def press_k2(self):
        self._native_next()

    def press_k3(self):
        self._native_previous()

    def press_k4(self):
        self._native_toggle_mode()


def get_app_manager():
    sonos_devices = discover()
    for s in sonos_devices:
        if s.player_name == DEFAULT_DEVICE_NAME:
            d = s
    return AppManager(
        d.get_current_transport_info()["current_transport_state"],
        d.volume,
        default_device=d,
    )
