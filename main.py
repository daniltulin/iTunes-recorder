#!/usr/bin/env python3

from time import sleep

from hijack import Jack
from iTunes import Tunes

import logging
logging.basicConfig(level=logging.DEBUG)

class Application:
    def __init__(self):
        self.tunes = Tunes()
        self.jack = Jack()

    def run(self):
        playlist = self.tunes['iPod\'s playlist']
        for track in playlist.tracks():
            logging.debug('{0}-{1}'.format(track.artist(), track.name()))
            self.jack.start_recording(track)
            self.tunes.play(track)
            self.tunes.stop()

app = Application()

try:
    app.run()
except Exception as e:
    logging.error(e)
finally:
    app.tunes.stop()
    app.jack.kill()
