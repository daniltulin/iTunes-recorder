#!/bin/usr/env python3

from time import sleep

from hijack import Jack
from iTunes import Tunes

class Application:
    def __init__(self):
        self.tunes = Tunes()
        self.jack = Jack()

    def run(self):
        playlist = self.tunes['iPod\'s playlist']
        for track in playlist:
            self.jack.start_recording(track)
            self.tunes.play(track)

app = Application()
app.run()
