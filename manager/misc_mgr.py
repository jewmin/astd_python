# -*- coding: utf-8 -*-
# 杂七杂八管理
from logging import getLogger
from manager.base_mgr import BaseMgr
from model.fete import Fete
from model.reward_info import RewardInfo
from model.global_func import GlobalFunc
from model.supper_market_dto import SupperMarketDto
from model.supper_market_dto import SupperMarketSpecialDto


class MiscMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory):
        super(MiscMgr, self).__init__(time_mgr, service_factory)
        self.logger = getLogger(self.__class__.__name__)

    #######################################
    # server begin
    #######################################
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
            GlobalFunc.get_short_readable(user.m_nGold), GlobalFunc.get_short_readable(user.m_nCopper)))

        if user.m_bHasVersionGift:
            self.get_service_factory().get_city_mgr().get_update_reward()

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

    #######################################
    # newGift begin
    #######################################
    def get_new_gift_list(self):
        url = "/root/newGift!getNewGiftList.action"
        data = {"type": 1}
        result = self.get_protocol_mgr().post_xml(url, data, "礼包")
        if result and result.m_bSucceed:
            if "weekendgift" in result.m_objResult:
                self.get_new_gift_reward(result.m_objResult["weekendgift"]["id"])
            if "gift" in result.m_objResult:
                if result.m_objResult["gift"]["intime"] == "1" and result.m_objResult["gift"]["statuts"] == "0":
                    self.get_new_gift_reward(result.m_objResult["gift"]["id"])

    def get_new_gift_reward(self, gift_id):
        url = "/root/newGift!getNewGiftReward.action"
        data = {"giftId": gift_id}
        result = self.get_protocol_mgr().post_xml(url, data, "领取礼包")
        if result and result.m_bSucceed:
            content = result.m_objResult.get("content", "无效奖励")
            self.logger.info("领取礼包，获得{}".format(content))

    #######################################
    # fete begin
    #######################################
    def fete(self):
        fete_list = list()
        free_all_fete = 0
        url = "/root/fete.action"
        result = self.get_protocol_mgr().get_xml(url, "祭祀神庙")
        if result and result.m_bSucceed:
            for v in result.m_objResult["fetelist"]["fete"]:
                f = Fete()
                f.handle_info(v)
                fete_list.append(f)
            free_all_fete = int(result.m_objResult["fetelist"].get("freeallfete", "0"))
        return fete_list, free_all_fete

    def do_fete(self, fete_id, fete_gold, fete_name):
        url = "/root/fete!dofete.action"
        data = {"feteId": fete_id}
        result = self.get_protocol_mgr().post_xml(url, data, "祭祀")
        if result and result.m_bSucceed:
            self.logger.info("花费{}金币祭祀{}".format(fete_gold, fete_name))
            gain = result.m_objResult["gains"]["gain"]
            if isinstance(gain, list):
                for v in gain:
                    self.logger.info("{}倍暴击，获得{}+{}".format(v["pro"], v["addtype"], v["addvalue"]))
            else:
                self.logger.info("{}倍暴击，获得{}+{}".format(gain["pro"], gain["addtype"], gain["addvalue"]))

    #######################################
    # task begin
    #######################################
    def get_new_per_day_task(self):
        url = "/root/task!getNewPerdayTask.action"
        result = self.get_protocol_mgr().get_xml(url, "日常任务")
        if result and result.m_bSucceed:
            day_box_state = result.m_objResult["dayboxstate"].split(",")
            for k, v in enumerate(day_box_state, 1):
                if v == "0":
                    self.open_day_box(k)
            if result.m_objResult["redpacketinfo"]["redpacket"] == "0":
                self.open_week_red_packet()
            user = self.get_protocol_mgr().get_user()
            user.set_task(result.m_objResult["task"])
            for task in result.m_objResult["task"]:
                if task["taskstate"] == "3":
                    self.get_new_per_day_task_reward(task["taskid"])

    def open_day_box(self, reward_id):
        url = "/root/task!openDayBox.action"
        data = {"rewardId": reward_id}
        result = self.get_protocol_mgr().post_xml(url, data, "开启宝箱")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"]["reward"])
            self.logger.info("开启日常任务活跃宝箱，获得{}".format(reward_info))

    def open_week_red_packet(self):
        url = "/root/task!openWeekRedPacket.action"
        result = self.get_protocol_mgr().get_xml(url, "活跃红包")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"]["reward"])
            self.logger.info("日常任务活跃红包开奖，获得{}".format(reward_info))

    def get_new_per_day_task_reward(self, reward_id):
        url = "/root/task!getNewPerdayTaskReward.action"
        data = {"rewardId": reward_id}
        result = self.get_protocol_mgr().post_xml(url, data, "日常任务领奖")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"]["reward"])
            self.logger.info("日常任务领奖，获得{}".format(reward_info))

    #######################################
    # officer begin
    #######################################
    def officer(self):
        url = "/root/officer.action"
        result = self.get_protocol_mgr().get_xml(url, "升官")
        if result and result.m_bSucceed:
            if result.m_objResult["savesalary_cd"] == "0":
                self.save_salary()

    def save_salary(self):
        url = "/root/officer!saveSalary.action"
        result = self.get_protocol_mgr().get_xml(url, "领取俸禄")
        if result and result.m_bSucceed:
            gain = int(result.m_objResult["gain"])
            troop = result.m_objResult["troop"]
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"]["reward"])
            self.logger.info("领取俸禄，获得银币+{}，{}，{}".format(GlobalFunc.get_short_readable(gain), troop, reward_info))

    #######################################
    # market begin
    #######################################
    def get_player_supper_market(self):
        url = "/root/market!getPlayerSupperMarket.action"
        result = self.get_protocol_mgr().get_xml(url, "集市")
        if result and result.m_bSucceed:
            supper_market_dto_list = list()
            if "suppermarketdto" in result.m_objResult:
                supper_market_dto = result.m_objResult["suppermarketdto"]
                if isinstance(supper_market_dto, list):
                    for v in supper_market_dto:
                        dto = SupperMarketDto()
                        dto.handle_info(v)
                        supper_market_dto_list.append(dto)
                else:
                    dto = SupperMarketDto()
                    dto.handle_info(supper_market_dto)
                    supper_market_dto_list.append(dto)
            supper_market_special_dto_list = list()
            if "special" in result.m_objResult:
                special = result.m_objResult["special"]
                if isinstance(special, list):
                    for v in special:
                        dto = SupperMarketSpecialDto()
                        dto.handle_info(v)
                        supper_market_special_dto_list.append(dto)
                else:
                    dto = SupperMarketSpecialDto()
                    dto.handle_info(special)
                    supper_market_special_dto_list.append(dto)
            for v in supper_market_special_dto_list:
                if v.state == 1:
                    self.buy_supper_market_special_goods(v.id)

    def buy_supper_market_special_goods(self, commodity_id):
        url = "/root/market!buySupperMarketSpecialGoods.action"
        data = {"commodityId": commodity_id}
        result = self.get_protocol_mgr().post_xml(url, data, "购买每日特供")
        if result and result.m_bSucceed:
            pass

    #######################################
    # tickets begin
    #######################################
    def tickets(self):
        url = "/root/tickets.action"
        result = self.get_protocol_mgr().get_xml(url, "点券")
        if result and result.m_bSucceed:
            pass
