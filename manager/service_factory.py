# -*- coding: utf-8 -*-
# 统一管理
from manager.time_mgr import TimeMgr
from manager.misc_mgr import MiscMgr
from manager.city_mgr import CityMgr
from manager.active_mgr import ActiveMgr
from manager.equip_mgr import EquipMgr
from manager.general_mgr import GeneralMgr
from manager.battle_mgr import BattleMgr
from manager.activity_mgr import ActivityMgr
from manager.world_mgr import WorldMgr


class ServiceFactory(object):
    def __init__(self, user, index):
        super(ServiceFactory, self).__init__()
        self.m_objProtocolMgr = None
        self.m_objTimeMgr = TimeMgr()
        self.m_objMiscMgr = MiscMgr(self.m_objTimeMgr, self, user, index)
        self.m_objCityMgr = CityMgr(self.m_objTimeMgr, self, user, index)
        self.m_objActiveMgr = ActiveMgr(self.m_objTimeMgr, self, user, index)
        self.m_objEquipMgr = EquipMgr(self.m_objTimeMgr, self, user, index)
        self.m_objGeneralMgr = GeneralMgr(self.m_objTimeMgr, self, user, index)
        self.m_objBattleMgr = BattleMgr(self.m_objTimeMgr, self, user, index)
        self.m_objActivityMgr = ActivityMgr(self.m_objTimeMgr, self, user, index)
        self.m_objWorldMgr = WorldMgr(self.m_objTimeMgr, self, user, index)

    def set_protocol_mgr(self, protocol_mgr):
        self.m_objProtocolMgr = protocol_mgr

    def get_protocol_mgr(self):
        return self.m_objProtocolMgr

    def get_time_mgr(self):
        return self.m_objTimeMgr

    def get_misc_mgr(self):
        return self.m_objMiscMgr

    def get_city_mgr(self):
        return self.m_objCityMgr

    def get_active_mgr(self):
        return self.m_objActiveMgr

    def get_equip_mgr(self):
        return self.m_objEquipMgr

    def get_general_mgr(self):
        return self.m_objGeneralMgr

    def get_battle_mgr(self):
        return self.m_objBattleMgr

    def get_activity_mgr(self):
        return self.m_objActivityMgr

    def get_world_mgr(self):
        return self.m_objWorldMgr
