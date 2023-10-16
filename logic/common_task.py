# -*- coding: utf-8 -*-
# 通用任务
from logic.base_task import BaseTask
from logic.config import config


class CommonTask(BaseTask):
    def __init__(self):
        super(CommonTask, self).__init__()
        self.m_szName = "common"
        self.m_szReadable = "通用"

    def run(self):
        self.init()
        return self.next_half_hour()

    def init(self):
        misc_mgr = self.m_objServiceFactory.get_misc_mgr()
        city_mgr = self.m_objServiceFactory.get_city_mgr()
        equip_mgr = self.m_objServiceFactory.get_equip_mgr()
        misc_mgr.get_server_time()
        misc_mgr.get_player_info_by_user_id("")
        # misc_mgr.get_extra_info()
        misc_mgr.get_player_extra_info2()
        city_mgr.get_main_city()
        equip_mgr.get_upgrade_info()

        # 登录奖励
        if config["mainCity"]["auto_get_login_reward"]:
            # 今日手气
            if self.m_objUser.m_bHasPerDayReward:
                city_mgr.get_per_day_reward()
            # 礼包
            misc_mgr.get_new_gift_list()
            # 登录签到送礼
            city_mgr.get_login_reward_info()
            # 恭贺
            city_mgr.get_champion_info()
            # 俸禄
            misc_mgr.officer()

        # 将军塔
        city_mgr.get_general_tower_info(config["mainCity"]["auto_build_general_tower"])

        # 免费征兵
        if config["mainCity"]["auto_right_army"]:
            if self.m_objUser.m_nRightNum > 0 and self.m_objUser.m_nRightCd == 0:
                city_mgr.right_army()

        # 日常任务
        if config["task"]["auto_task"]:
            misc_mgr.get_new_per_day_task()

        # 采集宝石
        if config["outCity"]["auto_end_bao_shi_pick"]:
            city_mgr.get_pick_space(config["outCity"]["end_pick_proportion"])

        # 自动领取军令
        if config["mainCity"]["auto_apply_token"]:
            misc_mgr.secretary()

        # 自动技术研究
        if config["outCity"]["auto_tech_research"]:
            city_mgr.jail(self.get_available_gold(), config["outCity"]["jail_baoshi"])

        # 自动委派
        if config["mainCity"]["auto_trade"]:
            misc_mgr.get_player_merchant()

        # 征收活动
        self.getEventGiftInfo()

    def getEventGiftInfo(self):
        url = "/root/gift!getEventGiftInfo.action"
        result = self.m_objProtocolMgr.get_xml(url, "征收活动")
        if result and result.m_bSucceed:
            rewardnum = result.m_objResult.get("rewardnum")
            if rewardnum:
                rewardnum = list(map(int, rewardnum[:-1].split(",")))
                for idx, reward in enumerate(rewardnum):
                    if reward == 1:
                        self.receiveEventReward(idx)

    def receiveEventReward(self, idx):
        url = "/root/gift!receiveEventReward.action"
        data = {"id": idx}
        result = self.m_objProtocolMgr.post_xml(url, data, "领取礼包")
        if result and result.m_bSucceed:
            ticket = int(result.m_objResult["message"])
            self.m_objServiceFactory.m_objMiscMgr.info("领取礼包, 获得点券+{}".format(ticket))
