from os import system

class LaunchException(Exception): pass

APP_PATH = '/Applications/iTunes.app/'

from collections.abc import Mapping
import appscript

from time import sleep

class Tunes(Mapping):
    def __init__(self):
        if system('open -a ' + APP_PATH) > 0:
            raise LaunchException()
        self.app = appscript.app("iTunes")
        self.stop()

    def play(self, track):
        self.app.play(track)
        while self.state == 'playing':
            sleep(.5)

    def stop(self):
        self.app.stop()

    @property
    def state(self):
        return str(self.app.player_state())[2:]

    @property
    def playlists(self):
        return self.app.playlists

    def __getitem__(self, key):
        return self.playlists[key]

    def __len__(self):
        return len(self.playlists)

    def __iter__(self):
        return self.playlists.__iter__()
