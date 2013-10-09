
from logging.handlers import BaseRotatingHandler
import string
import time
import datetime
import os


class TimePatternRotatingHandler(BaseRotatingHandler):
    def __init__(self, filename, when, encoding=None, delay=0):
        self.when = string.upper(when)
        self.fname_pat = filename
        self.mock_dt = None

        self.computeNextRollover()

        BaseRotatingHandler.__init__(self, self.filename, 'a', encoding, delay)

    def get_now_dt(self):
        if self.mock_dt is not None:
            return self.mock_dt

        return datetime.datetime.now()

    def computeNextRollover(self):
        now = self.get_now_dt()
        if self.when == 'MONTH':
            dtfmt = '%Y-%m'
            dt = (now.replace(day=1) + datetime.timedelta(days=40)).replace(day=1, hour=0, minute=0, second=0)
            rolloverAt = time.mktime(dt.timetuple())
        elif self.when == 'DAY':
            dtfmt = '%Y-%m-%d'
            dt = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0)
            rolloverAt = time.mktime(dt.timetuple())

        self.rolloverAt = rolloverAt
        self.dtfmt = dtfmt
        self.filename = os.path.abspath(self.fname_pat % (now.strftime(self.dtfmt)))
        #print now, self.filename

    def shouldRollover(self, record):
        now = self.get_now_dt()
        t = time.mktime(now.timetuple())
        #print t, self.rolloverAt

        if t >= self.rolloverAt:
            return 1
        return 0

    def doRollover(self):
        if self.stream:
            self.stream.close()

        self.computeNextRollover()
        self.baseFilename = self.filename

        self.stream = self._open()



