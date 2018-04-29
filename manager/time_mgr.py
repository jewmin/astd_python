# -*- coding: utf-8 -*-
# 时间管理
import time


class TimeMgr(object):
    def __init__(self):
        super(TimeMgr, self).__init__()
        self.m_nTimeSpan = 0

    def set_timestamp(self, server_timestamp):
        self.m_nTimeSpan = int(round(time.time() * 1000)) - server_timestamp

    def get_timestamp(self):
        return int(round(time.time() * 1000)) - self.m_nTimeSpan
