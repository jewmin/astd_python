# -*- coding: utf-8 -*-
# 中秋月饼
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo, Reward


class EatMoonCakeEvent(ActivityTask):
    def __init__(self):
        super(EatMoonCakeEvent, self).__init__(ActivityType.EatMoonCakeEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "中秋月饼"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_info()
        if info is None:
            return self.next_half_hour()

        for eat_state in info["吃货状态"]:
            if eat_state["state"] == "1":
                # self.get_progress_reward(eat_state["id"])
                pass

        if info["吃蛋黄月饼花费金币"] <= self.m_dictConfig["gold"]:
            self.eat_moon_cake(info["吃蛋黄月饼花费金币"], 1)
            return self.immediate()
        elif info["吃豆沙月饼花费金币"] <= self.m_dictConfig["gold"]:
            self.eat_moon_cake(info["吃豆沙月饼花费金币"], 2)
            return self.immediate()

        return self.next_half_hour()

    def get_info(self):
        url = "/root/eatMooncakeEvent!getInfo.action"
        result = self.get_xml(url, "中秋月饼")
        if result and result.m_bSucceed:
            info = dict()
            info["吃货状态"] = result.m_objResult["eatstate"]
            info["吃蛋黄月饼花费金币"] = int(result.m_objResult["cost1"])
            info["吃豆沙月饼花费金币"] = int(result.m_objResult["cost2"])
            return info
    
    def eat_moon_cake(self, cost, cake_type):
        cake_name = ("", "蛋黄", "豆沙")
        url = "/root/eatMooncakeEvent!eatMooncake.action"
        data = {"type": cake_type}
        result = self.post_xml(url, data, "吃月饼")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.consume_gold(cost)
            if cost > 0:
                use_gold = True
                msg = "花费{}金币".format(cost)
            else:
                use_gold = False
                msg = "免费"
            self.info("{}，吃{}月饼，获得{}".format(msg, cake_name[cake_type], reward_info), use_gold)

    def get_progress_reward(self, reward_id):
        url = "/root/eatMooncakeEvent!getProgressReward.action"
        data = {"rewardId": reward_id}
        result = self.post_xml(url, data, "领取月饼奖励")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("领取月饼奖励，获得{}".format(reward_info))
