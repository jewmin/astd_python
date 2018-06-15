# -*- coding: utf-8 -*-
# 百家宴
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo
from model.reward_info import Reward


class DuanWuEvent(ActivityTask):
    def __init__(self):
        super(DuanWuEvent, self).__init__(ActivityType.DuanWuEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "百家宴"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_duanwu_event_info()
        if info is None:
            return self.next_half_hour()

        for reward in info["奖励"]:
            if reward["state"] == "1":
                self.get_reward_by_id(reward, self.get_choice(reward["choice"]))

        if info["轮数"] > 0:
            if info["饥饿"] > 0:
                if info["普通粽子"] <= self.m_dictConfig["limit_hunger"]:
                    self.eat_zongzi(0, False)
                    return self.immediate()
                elif info["花费金币"] <= self.m_dictConfig["gold_hunger"] and info["花费金币"] <= self.get_available_gold():
                    self.eat_zongzi(info["花费金币"], True)
                    return self.immediate()
                else:
                    self.eat_zongzi(0, False)
                    return self.immediate()
            else:
                self.next_round()
                return self.immediate()
        elif info["购买轮数花费金币"] <= self.m_dictConfig["gold_round"] and info["购买轮数花费金币"] <= self.get_available_gold():
            self.buy_round(info["购买轮数花费金币"])
            return self.immediate()

        return self.next_half_hour()

    def get_duanwu_event_info(self):
        url = "/root/event!getDuanwuEventInfo.action"
        result = self.get_xml(url, "百家宴")
        if result and result.m_bSucceed:
            info = dict()
            info["奖励"] = result.m_objResult["rewards"]
            info["轮数"] = int(result.m_objResult["remainround"])
            info["购买轮数花费金币"] = int(result.m_objResult["buyroundcost"])
            info["普通粽子"] = int(result.m_objResult["zongziinfo"]["hunger"])
            info["金币粽子"] = int(result.m_objResult["zongziinfo"]["goldhunger"])
            info["花费金币"] = int(result.m_objResult["zongziinfo"]["goldcost"])
            info["饥饿"] = int(result.m_objResult["hunger"])
            return info

    def eat_zongzi(self, cost, use_gold):
        url = "/root/event!eatZongzi.action"
        data = {"gold": 1 if use_gold else 0}
        result = self.post_xml(url, data, "吃粽子")
        if result and result.m_bSucceed:
            reward = Reward()
            reward.type = 42
            reward.lv = 1
            reward.num = int(result.m_objResult["reward"]["tickets"])
            reward.itemname = "点券"
            reward_info = RewardInfo()
            reward_info.m_listRewards.append(reward)
            self.add_reward(reward_info)
            self.consume_gold(cost)
            self.info("花费{}金币，吃粽子，获得{}".format(cost, reward_info), use_gold)

    def buy_round(self, cost):
        url = "/root/event!buyRound.action"
        result = self.get_xml(url, "购买轮数")
        if result and result.m_bSucceed:
            self.info("花费{}金币，购买轮数".format(cost), True)

    def next_round(self):
        url = "/root/event!nextRound.action"
        result = self.get_xml(url, "再吃一轮")
        if result and result.m_bSucceed:
            self.info("再吃一轮")

    def get_reward_by_id(self, reward, db_id):
        url = "/root/event!getRewardById.action"
        data = {"rewardId": reward["id"], "dbId": db_id}
        result = self.post_xml(url, data, "领取奖励")
        if result and result.m_bSucceed:
            reward1 = Reward()
            reward1.type = 49
            reward1.lv = 1
            reward1.num = int(result.m_objResult["reward"]["bigginfo"]["num"])
            reward1.itemname = "大将令[{}]".format(result.m_objResult["reward"]["bigginfo"]["name"])
            reward2 = Reward()
            reward2.type = 42
            reward2.lv = 1
            reward2.num = int(result.m_objResult["reward"]["tickets"])
            reward2.itemname = "点券"
            reward_info = RewardInfo()
            reward_info.m_listRewards.append(reward1)
            reward_info.m_listRewards.append(reward2)
            self.add_reward(reward_info)
            self.info("领取奖励，获得{}".format(reward_info))

    def get_choice(self, choice):
        for v in choice:
            if v["bigginfo"]["name"] in self.m_dictConfig["general"]:
                return v["rewardid"]
        return choice[0]["rewardid"]
