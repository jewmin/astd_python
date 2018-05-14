# -*- coding: utf-8 -*-
# 管理基类
from logic.config import config


class BaseMgr(object):
    def __init__(self, time_mgr, service_factory):
        super(BaseMgr, self).__init__()
        self.m_objTimeMgr = time_mgr
        self.m_objServiceFactory = service_factory

    def get_protocol_mgr(self):
        return self.m_objServiceFactory.get_protocol_mgr()

    def get_service_factory(self):
        return self.m_objServiceFactory

    @staticmethod
    def get_impose_select_le(effect1, effect2):
        for v in config["impose"]["impose_event"]:
            if effect1.find(v) >= 0:
                return 1
            elif effect2.find(v) >= 0:
                return 2
