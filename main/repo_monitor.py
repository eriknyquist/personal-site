import time
import threading
import os

import poacher

HISTORY_LEN = 4

def mean(items):
    return sum(items) / len(items)

class PoacherMonitor(poacher.GithubPoacher):
    def __init__(self, *args, **kwargs):
        self.updatetime = None
        self.rpm = 0.0
        self.history = []
        super(PoacherMonitor, self).__init__(*args, **kwargs)

    def on_lock(self, repoid):
        self.updatetime = time.time()

    def on_repos_processed(self, num):
        minutes = (time.time() - self.updatetime) / 60.0
        rpm = float(num) / minutes
        self.history.append(rpm)

        if len(self.history) < 2:
            self.rpm = rpm
        else:
            if len(self.history) > HISTORY_LEN:
                del(self.history[0])

            self.rpm = mean(self.history)

        self.updatetime = time.time()

class ReposPerMinuteMonitor(object):
    def __init__(self, uname, pwd):
        self.monitor = PoacherMonitor(poll_delay_seconds=30, github_retries=10,
            github_retry_delay_seconds=2)

        self.monitor.authenticate(uname, pwd)
        self.task = threading.Thread(target=self._monitor_task)
        self.task.daemon = True

    def _monitor_task(self):
        self.monitor.main_loop(start_id=144242737)

    def start(self):
        if self.task.is_alive():
            return

        self.task.start()

    def rpm(self):
        return self.monitor.rpm
