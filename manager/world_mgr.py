# -*- coding: utf-8 -*-
# 世界管理
from manager.base_mgr import BaseMgr


class WorldMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(WorldMgr, self).__init__(time_mgr, service_factory, user, index)
        self.m_listAreas = list()  # 城池列表
        self.m_dictFengDi = dict()  # 封地
        self.m_dictDaoJu = dict()  # 道具
        self.m_nTreasureNum = 0  # 国家宝箱
        self.m_nCityHpRecoverCd = 0  # 城防恢复冷却时间
        self.m_nFreeClearMoveTime = 0  # 免费清除迁移冷却时间次数
        self.m_nTransferCd = 0  # 迁移冷却时间

    def set_feng_di(self, feng_di_info):
        self.m_dictFengDi.clear()
        self.m_dictFengDi["剩余封地生产次数"] = int(feng_di_info["remainnum"])
        self.m_dictFengDi["免费借兵次数"] = int(feng_di_info["freejiebinnum"])
        self.m_dictFengDi["金币借兵消耗"] = int(feng_di_info["jiebincost"])

    def set_dao_ju(self, dao_ju_info):
        self.m_dictDaoJu.clear()
        self.m_dictDaoJu["决斗战旗"] = int(dao_ju_info["flagnum"])
        self.m_dictDaoJu["诱敌锦囊"] = int(dao_ju_info["jinnum"])

    def get_new_area(self):
        url = "/root/world!getNewArea.action"
        result = self.get_protocol_mgr().get_xml(url, "世界")
        if result and result.m_bSucceed:
            self.set_feng_di(result.m_objResult["fengdi"])
            self.set_dao_ju(result.m_objResult["daoju"])
            self.m_nTreasureNum = int(result.m_objResult["treasurenum"])
            self.m_nCityHpRecoverCd = int(result.m_objResult["cityhprecovercd"])
            self.m_nFreeClearMoveTime = int(float(result.m_objResult["freeclearmovetime"]))
            self.m_nTransferCd = int(result.m_objResult["tranfercd"])
            self.m_listAreas = result.m_objResult["newarea"]

    def get_transfer_info(self):
        url = "/root/world!getTranferInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "迁移")
        if result and result.m_bSucceed:
            if result.m_objResult["canget"] == "1":
                self.get_transfer_token()

    def get_transfer_token(self):
        url = "/root/world!getTransferToken.action"
        result = self.get_protocol_mgr().get_xml(url, "领取攻击令")
        if result and result.m_bSucceed:
            self.info("领取{}攻击令".format(result.m_objResult["token"]))
