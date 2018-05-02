# -*- coding: utf-8 -*-
# 统一管理
from manager.time_mgr import TimeMgr
from manager.misc_mgr import MiscMgr


class ServiceFactory(object):
    def __init__(self):
        super(ServiceFactory, self).__init__()
        self.m_objProtocolMgr = None
        self.m_objTimeMgr = TimeMgr()
        self.m_objMiscMgr = MiscMgr(self.m_objTimeMgr, self)

    def set_protocol_mgr(self, protocol_mgr):
        self.m_objProtocolMgr = protocol_mgr

    def get_protocol_mgr(self):
        return self.m_objProtocolMgr

    def get_time_mgr(self):
        return self.m_objTimeMgr

    def get_misc_mgr(self):
        return self.m_objMiscMgr
