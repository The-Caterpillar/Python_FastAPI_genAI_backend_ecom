from datetime import timedelta, datetime
from datetime import datetime
import pytz


class TimerService:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start_timer(self):
        self.start_time = datetime.now()

    def end_timer(self):
        self.end_time = datetime.now()
        if self.start_time is None:
            raise RuntimeError("Timer has not started yet.")
        return self.end_time - self.start_time

    def get_time_difference(self):
        if self.start_time is None or self.end_time is None:
            raise RuntimeError("Timer has not started or ended yet.")
        return self.end_time - self.start_time