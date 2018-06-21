# -*- coding: utf-8 -*-
# 雪地通商
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class SnowTrading(ActivityTask):
    def __init__(self):
        super(SnowTrading, self).__init__(ActivityType.SnowTradingEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "雪地通商"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_snow_trading_info()
        if info is None:
            return self.next_half_hour()

        for case in info["奖励"]:
            if case["state"] == "1":
                self.get_case_num_reward(case)

        if info["免费通商次数"] > 0:
            if self.m_dictConfig["reinforce"]["enable"]:
                if not info["已加固雪橇"] and info["宝箱类型"] >= self.m_dictConfig["reinforce"]["type"] and info["加固雪橇花费金币"] <= self.m_dictConfig["reinforce"]["cost"] and info["加固雪橇花费金币"] <= self.get_available_gold():
                    self.reinforce_sled(info["加固雪橇花费金币"])
                    return self.immediate()
            self.transport(self.m_dictConfig["choose"], info["宝箱类型"])
            return self.immediate()
        elif info["购买次数花费金币"] <= self.m_dictConfig["buyroundcost"] and info["购买次数花费金币"] <= self.get_available_gold():
            self.buy_round(info["购买次数花费金币"])
            return self.immediate()

        return self.next_half_hour()

    def get_snow_trading_info(self):
        url = "/root/snowTrading!getSnowTradingInfo.action"
        result = self.get_xml(url, "雪地通商")
        if result and result.m_bSucceed:
            info = dict()
            info["加固雪橇花费金币"] = int(result.m_objResult["reinforcecost"])
            info["购买次数花费金币"] = int(result.m_objResult["buyroundcost"])
            info["免费通商次数"] = int(result.m_objResult["hastime"])
            info["奖励"] = result.m_objResult["casestate"]
            info["已加固雪橇"] = result.m_objResult["reinforce"] == "1"
            info["宝箱类型"] = int(result.m_objResult["casttype"])
            return info

    def get_case_num_reward(self, case):
        url = "/root/snowTrading!getCaseNumReward.action"
        data = {"cases": case["id"]}
        result = self.post_xml(url, data, "领取雪地通商奖励")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("领取雪地通商奖励，获得{}".format(reward_info))

    def buy_round(self, cost):
        url = "/root/snowTrading!buyRound.action"
        result = self.get_xml(url, "购买次数")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            self.info("花费{}金币，购买次数".format(cost), True)

    def reinforce_sled(self, cost):
        url = "/root/snowTrading!reinforceSled.action"
        result = self.get_xml(url, "加固雪橇")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            self.info("花费{}金币，加固雪橇".format(cost), True)

    def transport(self, choose, cast_type):
        cast_tuple = ("", "木质", "白银", "黄金")
        url = "/root/snowTrading!transport.action"
        data = {"choose": choose}
        result = self.post_xml(url, data, "雪地通商")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("雪地通商，掉落{}个{}宝箱，获得{}".format(result.m_objResult["stonestate"]["storneloss"], cast_tuple[cast_type], reward_info))
