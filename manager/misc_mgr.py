# -*- coding: utf-8 -*-
# 杂七杂八管理
from logging import getLogger
from manager.base_mgr import BaseMgr


class MiscMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory):
        super(MiscMgr, self).__init__(time_mgr, service_factory)
        self.logger = getLogger(self.__class__.__name__)

    def get_server_time(self):
        url = "/root/server!getServerTime.action"
        result = self.get_protocol_mgr().get_xml(url, "获取系统时间")
        if result and result.m_bSucceed:
            server_time = int(result.m_objResult["time"])
            self.m_objTimeMgr.set_timestamp(server_time)
            self.logger.debug("got timestamp = {}".format(server_time))

    def get_player_info_by_user_id(self, role_name):
        url = "/root/server!getPlayerInfoByUserId.action"
        result = self.get_protocol_mgr().get_xml(url, "获取玩家信息")
        if result is None or not result.m_bSucceed:
            self.logger.warning("获取用户信息失败，请重试")
            return False

        # 选择角色
        if result.m_objResult.get("op", "") == "xzjs":
            code = result.m_objResult["code"]
            for v in result.m_objResult["player"]:
                if role_name == v["playername"]:
                    player_id = v["playerid"]
                    break
            if player_id is None:
                self.logger.warning("您选择的角色不存在")
                return False

            if not self.choose_role(player_id, code):
                self.logger.warning("切换角色失败")
                return False

            result = self.get_protocol_mgr().get_xml(url, "获取玩家信息")
            if result is None or not result.m_bSucceed:
                self.logger.warning("获取用户信息失败，请重试")
                return False

        if "blockreason" in result.m_objResult:
            self.logger.warning("角色被封号，原因是：{}".format(result.m_objResult["blockreason"]))
            return False

        user = self.get_protocol_mgr().get_user()
        user.clear_activities()
        if "player" in result.m_objResult:
            user.refresh_player_info(result.m_objResult["player"])
        else:
            user.refresh_player_info(result.m_objResult["message"]["player"])
        if "limitvalue" in result.m_objResult:
            user.update_limits(result.m_objResult["limitvalue"])
        else:
            user.update_limits(result.m_objResult["message"]["limitvalue"])

        self.logger.info("{}({}级，{})，{}年{}，{}金币，{}银币".format(
            user.m_szUserName, user.m_nLevel, user.m_szNation,
            user.m_nYear, user.m_szSeason,
            user.m_nGold, user.m_nCopper))

        if user.m_bHasVersionGift:
            self.get_service_factory().get_city_mgr().get_update_reward()

        # if user.m_bHasPerDayReward:
        #     self.get_service_factory().get_city_mgr().get_per_day_reward()

        return True

    def choose_role(self, player_id, code):
        url = "/root/server!chooseRole.action"
        data = {"playerId": player_id, "code": code}
        result = self.get_protocol_mgr().post_xml(url, data, "选择玩家角色")
        if result and result.m_bSucceed:
            self.logger.info("选择角色成功")
            return True

    def get_extra_info(self):
        url = "/root/server!getExtraInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "获取玩家额外信息")
        if result and result.m_bSucceed:
            user = self.get_protocol_mgr().get_user()
            user.update_player_extra_info(result.m_objResult["player"])

    def get_player_extra_info2(self):
        url = "/root/server!getPlayerExtraInfo2.action"
        result = self.get_protocol_mgr().get_xml(url, "获取玩家额外信息")
        if result and result.m_bSucceed:
            user = self.get_protocol_mgr().get_user()
            user.update_player_extra_info2(result.m_objResult["player"])

    def get_new_gift_list(self):
        url = "/root/newGift!getNewGiftList.action"
        data = {"type": 1}
        result = self.get_protocol_mgr().post_xml(url, data, "获取登录礼包列表")
        if result and result.m_bSucceed:
            if "weekendgift" in result.m_objResult:
                self.get_new_gift_reward(result.m_objResult["weekendgift"]["id"])

    def get_new_gift_reward(self, gift_id):
        url = "/root/newGift!getNewGiftReward.action"
        data = {"giftId": gift_id}
        result = self.get_protocol_mgr().post_xml(url, data, "领取登录礼包")
        if result and result.m_bSucceed:
            content = result.m_objResult.get("content", "无效奖励")
            self.logger.info("领取登录礼包，获得{}".format(content))
