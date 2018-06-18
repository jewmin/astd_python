# -*- coding: utf-8 -*-
# 群雄煮酒
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class QingMingEvent(ActivityTask):
    def __init__(self):
        super(QingMingEvent, self).__init__(ActivityType.QingMingEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "群雄煮酒"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_qingming_info()
        if info is None:
            return self.next_half_hour()

        if info["大奖"]:
            self.get_qingming_big_reward()
            return self.immediate()
        elif info["轮数"] > 0:
            idx = 0
            for general in info["武将"]:
                if general["state"] == "1":
                    idx += 1
                else:
                    break
            info["酒"] = sorted(info["酒"], key=lambda obj: int(obj["winenum"]), reverse=True)
            for wine in info["酒"]:
                wine_num = int(wine["winenum"])
                if wine_num + info["醉意"] <= self.m_dictConfig["drink"][idx]:
                    self.qingming_drink(wine["id"], False)
                    return self.immediate()
                elif wine_num == 40 and info["酒仙附体花费金币"] <= self.m_dictConfig["golddrinkcost"] and info["酒仙附体花费金币"] <= self.get_available_gold():
                    self.qingming_drink(wine["id"], True, info["酒仙附体花费金币"])
                    return self.immediate()
            if int(info["酒"][2]["winenum"]) + info["醉意"] >= info["最大醉意"]:
                self.qingming_drink(info["酒"][0]["id"], False)
            else:
                self.qingming_drink(info["酒"][2]["id"], False)
            return self.immediate()
        elif info["购买轮数花费金币"] <= self.m_dictConfig["buycost"] and info["购买轮数花费金币"] <= self.get_available_gold():
            self.buy_qingming_round(info["购买轮数花费金币"])
            return self.immediate()

        return self.next_half_hour()

    def get_qingming_info(self):
        url = "/root/event!getQingmingInfo.action"
        result = self.get_xml(url, "群雄煮酒")
        if result and result.m_bSucceed:
            info = dict()
            info["购买轮数花费金币"] = int(result.m_objResult["buycost"])
            info["酒仙附体花费金币"] = int(result.m_objResult["golddrinkcost"])
            info["醉意"] = int(result.m_objResult["winenum"])
            info["最大醉意"] = int(result.m_objResult["maxnum"])
            info["轮数"] = int(result.m_objResult["roundnum"])
            info["酒"] = result.m_objResult["wineinfo"]["wine"]
            info["大奖"] = result.m_objResult.get("havebigreward", "0") == "1"
            info["武将"] = result.m_objResult["generalinfo"]
            return info

    def get_qingming_big_reward(self):
        url = "/root/event!getQingmingBigReward.action"
        result = self.get_xml(url, "群雄煮酒大礼")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("领取群雄煮酒大礼，获得{}".format(reward_info))

    def buy_qingming_round(self, cost):
        url = "/root/event!buyQingmingRound.action"
        result = self.get_xml(url, "购买群雄煮酒轮数")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            self.info("花费{}金币，购买群雄煮酒轮数".format(cost), True)

    def qingming_drink(self, wine_id, use_gold, cost=0):
        url = "/root/event!qingmingDrink.action"
        data = {"wineId": wine_id, "gold": 1 if use_gold else 0}
        result = self.post_xml(url, data, "饮酒")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.consume_gold(cost)
            if use_gold:
                self.info("花费{}金币，使用酒仙附体，饮酒，获得{}".format(cost, reward_info), True)
            else:
                self.info("免费饮酒，获得{}".format(reward_info))
