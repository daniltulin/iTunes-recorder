#!/usr/bin/env python3

from time import sleep

from hijack import Jack, does_contain_track
from iTunes import Tunes

import logging
logging.basicConfig(level=logging.DEBUG)

class Application:
    def __init__(self):
        self.tunes = Tunes()
        self.jack = Jack()

    def run(self, playlist_names):
        folder_path = '~/Music/iPod'
        for playlist_name in playlist_names:
            playlist = self.tunes[playlist_name]
            for track in playlist.tracks():
                if does_contain_track(folder_path, track):
                    continue
                logging.debug('{0} - {1}'.format(track.artist(), track.name()))
                self.jack.start_recording(folder_path, track)
                sleep(.4)
                self.tunes.play(track)
                self.tunes.stop()

app = Application()

try:
    app.run(['iPod\'s playlist'])
except Exception as e:
    logging.error(e)
finally:
    app.tunes.stop()
    app.jack.kill()
