# -*- coding: utf-8 -*-
# 统一管理
from manager.time_mgr import TimeMgr


class ServiceFactory(object):
    def __init__(self):
        super(ServiceFactory, self).__init__()
        self.m_objTimeMgr = TimeMgr()

    def get_time_mgr(self):
        return self.m_objTimeMgr
