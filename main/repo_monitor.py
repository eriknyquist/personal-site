import time
import threading
import struct
import os

import poacher

HISTORY_LEN = 4
BUFFER_LEN = 50
RECORD_FILE = "/opt/github_rpm_record.bin"

samples = []

def mean(items):
    return sum(items) / len(items)

def write_samples(samples):
    data = bytes(b'').join([struct.pack('!Qff', int(t), f, r) for t, f, r in samples])
    with open(RECORD_FILE, 'ab') as fh:
        fh.write(data)

def record_sample(timestamp, fpm, rpm):
    samples.append((int(timestamp), fpm, rpm))

    if len(samples) >= BUFFER_LEN:
        write_samples(samples)
        del samples[:]

class PoacherMonitor(poacher.GithubPoacher):
    def __init__(self, *args, **kwargs):
        self.updatetime = None
        self.rpm = 0.0
        self.fpm = 0.0
        self.forks = 0
        self.repos = 0
        self.url = None
        self.furl = None
        self.history = [[], []]
        super(PoacherMonitor, self).__init__(*args, **kwargs)

    def on_lock(self, repoid):
        self.updatetime = time.time()

    def on_repo(self, repo):
        if repo.fork:
            self.forks += 1
            try:
                self.furl = repo.clone_url
            except:
                pass
        else:
            self.repos += 1
            try:
                self.url = repo.clone_url
            except:
                pass

    def on_repos_processed(self, num):
        minutes = (time.time() - self.updatetime) / 60.0
        rpm = float(self.repos) / minutes
        fpm = float(self.forks) / minutes
        self.history[0].append(fpm)
        self.history[1].append(rpm)

        if len(self.history[0]) < 2:
            self.rpm = rpm
            self.fpm = fpm
        else:
            if len(self.history) > HISTORY_LEN:
                del(self.history[0][0])
                del(self.history[1][0])

            self.fpm = mean(self.history[0])
            self.rpm = mean(self.history[1])

        self.repos = 0
        self.forks = 0
        self.updatetime = time.time()
        record_sample(self.updatetime, self.fpm, self.rpm)

class ReposPerMinuteMonitor(object):
    def __init__(self, uname, pwd):
        self.monitor = PoacherMonitor(poll_delay_seconds=10, github_retries=0,
            github_retry_delay_seconds=30)

        self.monitor.authenticate(uname, pwd)
        self.task = threading.Thread(target=self._monitor_task)
        self.task.daemon = True

    def _monitor_task(self):
        self.monitor.main_loop(start_id=144242737)

    def start(self):
        if self.task.is_alive():
            return

        self.task.start()

    def url(self):
        return self.monitor.url

    def furl(self):
        return self.monitor.furl

    def rpm(self):
        return self.monitor.rpm

    def fpm(self):
        return self.monitor.fpm
