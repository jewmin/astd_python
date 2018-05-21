# -*- coding: utf-8 -*-
# 时间管理
import time
from datetime import datetime
import pytz


class TimeMgr(object):
    def __init__(self):
        super(TimeMgr, self).__init__()
        self.m_nTimeSpan = 0

    def set_timestamp(self, server_timestamp):
        self.m_nTimeSpan = int(round(time.time() * 1000)) - server_timestamp

    def get_timestamp(self):
        return int(round(time.time() * 1000)) - self.m_nTimeSpan

    # year, month, day, hour, minute, second, microsecond
    def get_datetime(self):
        return datetime.fromtimestamp(self.get_timestamp() / 1000, pytz.timezone("UTC"))

    @staticmethod
    def get_datetime_string(microseconds):
        dt = datetime.fromtimestamp(microseconds / 1000, pytz.timezone("UTC"))
        return "{}:{}:{}".format(dt.hour, dt.minute, dt.second)
