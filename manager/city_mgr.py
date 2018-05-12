# -*- coding: utf-8 -*-
# 城池管理
from logging import getLogger
from manager.base_mgr import BaseMgr
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo
from model.general_tower import GeneralTower


class CityMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory):
        super(CityMgr, self).__init__(time_mgr, service_factory)
        self.logger = getLogger(self.__class__.__name__)

    def get_main_city(self):
        url = "/root/mainCity.action"
        result = self.get_protocol_mgr().get_xml(url, "获取主城信息")
        if result and result.m_bSucceed:
            user = self.get_protocol_mgr().get_user()
            user.m_nRemainSeniorSlaves = int(result.m_objResult.get("remainseniorslaves", "0"))
            user.m_bCanVisit = result.m_objResult.get("canvisit", "0") == "1"
            user.m_bNewTechnology = result.m_objResult.get("newtechnology", "0") == "1"
            user.m_bWarChariot = result.m_objResult.get("warchariot", "0") == "1"
            self.set_activities(user, result.m_objResult)
            user.set_main_city_dto(result.m_objResult.get("maincitydto", []))
            user.set_constructor_dto(result.m_objResult.get("constructordto", []))
            user.set_mo_zi_building(result.m_objResult.get("mozibuilding", []))

    @staticmethod
    def set_activities(user, dict_activities_info):
        if dict_activities_info.get("hasarchevent", "0") == "1":
            user.m_dictActivities[ActivityType.HasArchEvent] = True
        if dict_activities_info.get("weekendgift", "0") == "1":
            user.m_dictActivities[ActivityType.WeekendGift] = True
        if dict_activities_info.get("shenhuo", "0") == "1":
            user.m_dictActivities[ActivityType.ShenHuo] = True
        if dict_activities_info.get("baishen", "0") == "1":
            user.m_dictActivities[ActivityType.BaiShen] = True
        if dict_activities_info.get("yang", "0") == "1":
            user.m_dictActivities[ActivityType.Yang] = True
        if dict_activities_info.get("offlineevent", "0") == "1":
            user.m_dictActivities[ActivityType.OfflineEvent] = True
        if dict_activities_info.get("arrestevent", "0") == "1":
            user.m_dictActivities[ActivityType.ArrestEvent] = True
        if dict_activities_info.get("goldticketevent", "0") == "1":
            user.m_dictActivities[ActivityType.GoldTicketEvent] = True
        if dict_activities_info.get("yuebingevent", "0") == "1":
            user.m_dictActivities[ActivityType.YueBingEvent] = True
        if dict_activities_info.get("boatevent", "0") == "1":
            user.m_dictActivities[ActivityType.BoatEvent] = True
        if dict_activities_info.get("buffevent", "0") == "1":
            user.m_dictActivities[ActivityType.BuffEvent] = True
        if dict_activities_info.get("cuilianevent", "0") == "1":
            user.m_dictActivities[ActivityType.CuiLianEvent] = True
        if dict_activities_info.get("payhongbaoevent", "0") == "1":
            user.m_dictActivities[ActivityType.PayHongBaoEvent] = True
        if dict_activities_info.get("bgevent", "0") == "1":
            user.m_dictActivities[ActivityType.BGEvent] = True
        if dict_activities_info.get("qingmingevent", "0") == "1":
            user.m_dictActivities[ActivityType.QingMingEvent] = True
        if dict_activities_info.get("duanwuevent", "0") == "1":
            user.m_dictActivities[ActivityType.DuanWuEvent] = True
        if dict_activities_info.get("moongeneralevent", "0") == "1":
            user.m_dictActivities[ActivityType.MoonGeneralEvent] = True
        if dict_activities_info.get("trainingevent", "0") == "1":
            user.m_dictActivities[ActivityType.TrainingEvent] = True
        if dict_activities_info.get("snowtradingevent", "0") == "1":
            user.m_dictActivities[ActivityType.SnowTradingEvent] = True
        if dict_activities_info.get("bombnianevent", "0") == "1":
            user.m_dictActivities[ActivityType.BombNianEvent] = True
        if dict_activities_info.get("borrowingarrowsevent", "0") == "1":
            user.m_dictActivities[ActivityType.BorrowingArrowsEvent] = True
        if dict_activities_info.get("paradeevent", "0") == "1":
            user.m_dictActivities[ActivityType.ParadeEvent] = True
        if dict_activities_info.get("towerstage", "0") == "1":
            user.m_dictActivities[ActivityType.TowerStage] = True
        if dict_activities_info.get("moontowerevent", "0") == "1":
            user.m_dictActivities[ActivityType.MoonTowerEvent] = True
        if dict_activities_info.get("goldboxevent", "0") == "1":
            user.m_dictActivities[ActivityType.GoldBoxEvent] = True
        if dict_activities_info.get("nationdaygoldboxevent", "0") == "1":
            user.m_dictActivities[ActivityType.NationDayGoldBoxEvent] = True
        if dict_activities_info.get("hasdaytreasuregame", "0") == "1":
            user.m_dictActivities[ActivityType.HasDayTreasureGame] = True
        if dict_activities_info.get("hastroopfeedback", "0") == "1":
            user.m_dictActivities[ActivityType.HasTroopFeedback] = True
        if dict_activities_info.get("hascakeevent", "false") == "true":
            user.m_dictActivities[ActivityType.HasCakeEvent] = True
        if dict_activities_info.get("hasnationdayevent", "0") == "1":
            user.m_dictActivities[ActivityType.HasNationDayEvent] = True
        if dict_activities_info.get("hasjailevent", "0") == "1":
            user.m_dictActivities[ActivityType.HasJailEvent] = True
        if dict_activities_info.get("showkfyz", "0") != "0":
            user.m_dictActivities[ActivityType.ShowKfYZ] = True
        if dict_activities_info.get("showkfwd", "0") != "0":
            user.m_dictActivities[ActivityType.ShowKfWD] = True
        if dict_activities_info.get("showkfpvp", "0") != "0":
            user.m_dictActivities[ActivityType.ShowKfPVP] = True

    def get_update_reward(self):
        url = "/root/mainCity!getUpdateReward.action"
        result = self.get_protocol_mgr().get_xml(url, "领取版本更新奖励")
        if result and result.m_bSucceed:
            user = self.get_protocol_mgr().get_user()
            user.m_bHasVersionGift = False

    def get_per_day_reward(self):
        url = "/root/mainCity!getPerDayReward.action"
        result = self.get_protocol_mgr().get_xml(url, "试试手气")
        if result and result.m_bSucceed:
            user = self.get_protocol_mgr().get_user()
            user.m_bHasPerDayReward = False
            gold = result.m_objResult["gold"]
            goldxs = result.m_objResult["goldxs"]
            token = result.m_objResult["token"]
            tokenxs = result.m_objResult["tokenxs"]
            self.logger.info("试试手气，获得{}金币({}倍暴击)，{}军令({}倍暴击)".format(gold, goldxs, token, tokenxs))

    def get_login_reward_info(self):
        url = "/root/mainCity!getLoginRewardInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "获取登录送礼")
        if result and result.m_bSucceed:
            if result.m_objResult["lastmonth"]["state15"] == "1":
                self.get_reward(1, 1)
            if result.m_objResult["lastmonth"]["statefull"] == "1":
                self.get_reward(1, 2)
            if result.m_objResult["curmonth"]["state15"] == "1":
                self.get_reward(2, 1)
            if result.m_objResult["curmonth"]["statefull"] == "1":
                self.get_reward(2, 2)

    def get_reward(self, cid, opt):
        url = "/root/mainCity!getReward.action"
        data = {"cId": cid, "opt": opt}
        result = self.get_protocol_mgr().post_xml(url, data, "领取登录送礼")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.logger.info("领取登录送礼，获得{}".format(str(reward_info)))

    def get_champion_info(self):
        url = "/root/mainCity!getChampionInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "争霸风云榜")
        if result and result.m_bSucceed:
            if result.m_objResult["canvisit"] == "1":
                self.visit_champion()

    def visit_champion(self):
        url = "/root/mainCity!visitChampion.action"
        result = self.get_protocol_mgr().get_xml(url, "恭贺")
        if result and result.m_bSucceed:
            self.logger.info("恭贺，获得点卷+{}".format(result.m_objResult["tickets"]))

    def get_general_tower_info(self):
        url = "/root/mainCity!getGeneralTowerInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "将军塔")
        if result and result.m_bSucceed:
            tower = GeneralTower()
            tower.handle_info(result.m_objResult["generaltower"])
            while tower.buildingstone > 0:
                self.use_building_stone(tower)

    def use_building_stone(self, tower):
        url = "/root/mainCity!useBuildingStone.action"
        result = self.get_protocol_mgr().get_xml(url, "筑造将军塔")
        if result and result.m_bSucceed:
            tower.handle_info(result.m_objResult["generaltower"])
            string = "筑造将军塔，进度增加{}".format(tower.addprogress)
            if tower.levelup == 1:
                string += "，升级"
            self.logger.info(string)
            self.logger.info("{}级将军塔({}/{})，剩余{}筑造石".format(tower.generaltowerlevel, tower.buildingprogress, tower.leveluprequirement, tower.buildingstone))
        else:
            tower.buildingstone = 0
