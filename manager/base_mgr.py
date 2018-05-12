# -*- coding: utf-8 -*-
# 管理基类


class BaseMgr(object):
    def __init__(self, time_mgr, service_factory):
        super(BaseMgr, self).__init__()
        self.m_objTimeMgr = time_mgr
        self.m_objServiceFactory = service_factory

    def get_protocol_mgr(self):
        return self.m_objServiceFactory.get_protocol_mgr()

    def get_service_factory(self):
        return self.m_objServiceFactory
