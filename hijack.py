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
    def __init__(self, track, session):
        now = datetime.now()
        single_date = datetime(now.year, now.month, now.day, 0, 0)
        start_time = now - single_date
        super(Event, self).__init__(scheduleRepeatDays=0,
                                    scheduleMode=0,
                                    scheduleEnabled=True,
                                    scheduleSingleDate=single_date,
                                    scheduleDuration=track.duration() + 1,
                                    scheduleQuitSources=False)
        self['sessionUUID'] = session['sessionUUID']
        self['scheduleStartTime'] = start_time.seconds

class Session(dict):
    def __init__(self, session, folder_path, track):
        super(Session, self).__init__(session)
        session_data = self['sessionData']
        blocks = session_data['geBlocks']
        recorder = blocks[1] # 0 is iTunes app block
        properties = recorder['geNodeProperties']
        file_name= '{0}_{1}'.format(track.artist(),
                                    track.name()).replace(' ', '_')
        properties['fileName'] = file_name
        properties['folderPathWithTilde'] = folder_path

        tags = properties['tagsPlist']
        tags['Artist'] = track.artist()
        tags['Title'] = track.name()
        tags['Year'] = track.year()
        tags['Album'] = track.album()

        logging.debug('Write filename ' + file_name)

class Jack:
    def start_recording(self, folder_path, track):
        self.kill()

        with open(SESSIONS_PATH, 'rb') as f:
            sessions = load(f)
            session, = sessions['modelItems']
        new_session = Session(session, folder_path, track)
        sessions['modelItems'] = [new_session]
        with open(SESSIONS_PATH, 'wb') as f:
            dump(sessions, f)

        with open(SCHEDULE_PATH, 'rb') as f:
            schedule = load(f)
        schedule['modelItems'] = [Event(track, new_session)]
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
