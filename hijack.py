from os import system, path
from subprocess import Popen, PIPE
from os.path import join
from datetime import datetime
from plistlib import dump, load
import logging

class LaunchException(Exception): pass

APP_PATH = '/Applications/Audio\ Hijack.app'
META_PATH = path.expanduser('~/Library/Application Support/Audio Hijack')

SCHEDULE_PATH = join(META_PATH, 'Schedule.plist')
SESSIONS_PATH = join(META_PATH, 'Sessions.plist')

class Event(dict):
    def __init__(self, track):
        now = datetime.now()
        single_date = datetime(now.year, now.month, now.day, 0, 0)
        start_time = now - single_date
        super(Event, self).__init__(scheduleRepeatDays=0,
                                    scheduleMode=0,
                                    scheduleEnabled=True,
                                    scheduleSingleDate=single_date,
                                    scheduleDuration=track.duration() + 1,
                                    scheduleQuitSources=False)
        self['sessionUUID'] = '0B2BCFF7-2D43-4F74-A393-FDAADCA633B8'
        self['scheduleStartTime'] = start_time.seconds

class Session(dict):
    def __init__(self, session, track):
        super(Session, self).__init__(session)
        session_data = self['sessionData']
        blocks = session_data['geBlocks']
        recorder = blocks[1] # 0 is iTunes app block
        properties = recorder['geNodeProperties']
        file_name= '{0}_{1}'.format(track.artist(),
                                    track.name())
        properties['fileName'] = file_name
        logging.debug('Write filename ' + file_name)

class Jack:
    def start_recording(self, track):
        self.kill()
        with open(SCHEDULE_PATH, 'rb') as f:
            schedule = load(f)
        schedule['modelItems'] = [Event(track)]
        with open(SCHEDULE_PATH, 'wb') as f:
            dump(schedule, f)
        self.launch()

    def launch(self):
        if system('open -a ' + APP_PATH) > 0:
            raise LaunchException()

    def kill(self):
        p = Popen(['ps', '-A'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out_raw, _ = p.communicate()
        out = out_raw.decode()

        pids = []

        for line in out.split('\n'):
            if 'Hijack' in line and not 'Helper' in line:
                pids.append(line.split()[0])

        for pid in pids:
            system('kill ' + str(pid))
