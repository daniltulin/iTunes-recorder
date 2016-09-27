
from os import system, path
from subprocess import Popen, PIPE


APP_PATH = '/Applications/Audio\ Hijack.app/'
META_PATH = path.expanduser('~/Library/Application\ Support/Audio\ Hijack/')

class LaunchError(Exception): pass

class Jack:
    def start_recording(self, track):
        self.kill()

        self.start()

    def launch(self):
        if system('open -a ' + APP_PATH) > 0:
            raise LaunchError()

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
