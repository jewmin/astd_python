# -*- coding: utf-8 -*-
# 武将管理
from manager.base_mgr import BaseMgr


class GeneralMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(GeneralMgr, self).__init__(time_mgr, service_factory, user, index)

    def get_refresh_general_info(self):
        url = "/root/general!getRefreshGeneralInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "培养")
        if result and result.m_bSucceed:
            pass
