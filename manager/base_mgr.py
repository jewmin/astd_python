# -*- coding: utf-8 -*-
# 管理基类


class BaseMgr(object):
    def __init__(self, time_mgr, service_factory):
        super(BaseMgr, self).__init__()
        self.m_objTimeMgr = time_mgr
        self.m_objServiceFactory = service_factory

    def get_protocol_mgr(self):
        return self.m_objServiceFactory.get_protocol_mgr()

    @staticmethod
    def immediate():
        return 2000

    @staticmethod
    def an_hour_later():
        return 3600000

    def next_half_hour(self):
        """距离下一半点相差的毫秒数"""
        minute = self.m_objTimeMgr.get_datetime().minute
        if minute < 30:
            remainder = 30 - minute
        else:
            remainder = 60 - minute
        return remainder * 60000

    def next_hour(self):
        """距离下一整点相差的毫秒数"""
        return (60 - self.m_objTimeMgr.get_datetime().minute) * 60000

    def next_day(self, next_hour=5):
        """距离第二天相差的毫秒数"""
        datetime = self.m_objTimeMgr.get_datetime()
        if datetime.hour < next_hour:
            remainder = next_hour - datetime.hour - 1
        else:
            remainder = 24 + next_hour - datetime.hour - 1
        return (remainder * 60 + 90 - datetime.minute) * 60000

    def next_dinner(self):
        """距离下一次宴会相差的毫秒数"""
        datetime = self.m_objTimeMgr.get_datetime()
        if datetime.hour < 10:
            remainder = 10 - datetime.hour - 1
        elif datetime.hour < 19:
            remainder = 19 - datetime.hour - 1
        else:
            remainder = 34 - datetime.hour - 1
        return (remainder * 60 + 90 - datetime.minute) * 60000
