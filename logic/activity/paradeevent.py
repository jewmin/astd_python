# -*- coding: utf-8 -*-
# 阅兵庆典
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class ParadeEvent(ActivityTask):
    def __init__(self):
        super(ParadeEvent, self).__init__(ActivityType.ParadeEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "阅兵庆典"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_parad_event_info()
        if info is None:
            return self.next_half_hour()

        for parade_state in info["奖励"]:
            if parade_state["state"] == "1":
                self.get_parade_reward(parade_state)

        if info["免费阅兵轮数"] <= 0:
            if info["购买轮数花费金币"] <= self.m_dictConfig["round_cost"] and info["购买轮数花费金币"] <= self.get_available_gold():
                self.add_round_times(info["购买轮数花费金币"])
                return self.immediate()
            else:
                return self.next_half_hour()

        while info["免费阅兵次数"] > 0:
            info["免费阅兵次数"] -= 1
            self.parade_army(0)
        self.get_next_general()

        return self.immediate()

    def get_parad_event_info(self):
        url = "/root/paradeEvent!getParadeEventInfo.action"
        result = self.get_xml(url, "阅兵庆典")
        if result and result.m_bSucceed:
            info = dict()
            info["免费阅兵次数"] = int(result.m_objResult["freetimes"])
            info["免费阅兵轮数"] = int(result.m_objResult["freeroundtimes"])
            info["阅兵花费金币"] = int(result.m_objResult["cost"])
            info["购买轮数花费金币"] = int(result.m_objResult["roundcost"])
            info["奖励"] = result.m_objResult["paradestate"]
            return info

    def get_parade_reward(self, parade_state):
        url = "/root/paradeEvent!getParadeReward.action"
        data = {"rewardId": parade_state["id"]}
        result = self.post_xml(url, data, "领取阅兵奖励")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("领取阅兵奖励，获得{}".format(reward_info))

    def add_round_times(self, cost):
        url = "/root/paradeEvent!addRoundTimes.action"
        result = self.get_xml(url, "购买阅兵轮数")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            self.info("花费{}金币，购买阅兵轮数".format(cost), True)

    def parade_army(self, cost):
        url = "/root/paradeEvent!paradeArmy.action"
        result = self.get_xml(url, "开始阅兵")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.consume_gold(cost)
            if cost > 0:
                msg = "花费{}金币，开始阅兵".format(cost)
                use_gold = True
            else:
                msg = "免费开始阅兵"
                use_gold = False
            msg += "，获得{}".format(reward_info)
            if "bigreward" in result.m_objResult:
                big_reward_info = RewardInfo()
                big_reward_info.handle_info(result.m_objResult["bigreward"]["rewardinfo"])
                self.add_reward(big_reward_info)
                msg += " {}".format(big_reward_info)
            self.info(msg, use_gold)

    def get_next_general(self):
        url = "/root/paradeEvent!getNextGeneral.action"
        result = self.get_xml(url, "下一位武将")
        if result and result.m_bSucceed:
            self.info("下一位武将[{}]准备阅兵".format(result.m_objResult["generalname"]))
