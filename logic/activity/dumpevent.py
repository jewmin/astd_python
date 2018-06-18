# -*- coding: utf-8 -*-
# 宝石倾销
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo, Reward


class DumpEvent(ActivityTask):
    def __init__(self):
        super(DumpEvent, self).__init__(ActivityType.DumpEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "宝石倾销"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_detail()
        if info is None:
            return self.next_half_hour()

        while info["商品"]["numleft"] > 0:
            info["商品"]["numleft"] -= 1
            self.buy(info["商品"])

        while info["锦囊"] > 0:
            info["锦囊"] -= 20
            self.open_bags(20)

        return self.next_half_hour()

    def get_detail(self):
        url = "/root/dumpEvent!getDetail.action"
        result = self.get_xml(url, "宝石倾销")
        if result and result.m_bSucceed:
            info = dict()
            info["锦囊"] = int(result.m_objResult["totalbags"])
            info["商品"] = result.m_objResult["goodlist"]["good"][0]
            info["商品"]["numleft"] = int(info["商品"]["numleft"])
            return info

    def buy(self, good):
        url = "/root/dumpEvent!buy.action"
        data = {"id": good["id"]}
        result = self.post_xml(url, data, "购买")
        if result and result.m_bSucceed:
            reward = Reward()
            reward.type = 5
            reward.lv = int(good["baoshilevel"])
            reward.itemname = "宝石"
            reward.num = 1
            reward_info = RewardInfo()
            reward_info.m_listRewards.append(reward)
            self.add_reward(reward_info)
            self.info("花费{}点券，获得{}个锦囊 {}".format(good["cost"], good["extrabags"], reward_info))

    def open_bags(self, num):
        url = "/root/dumpEvent!openBags.action"
        data = {"num": num}
        result = self.post_xml(url, data, "开启锦囊")
        if result and result.m_bSucceed:
            reward = Reward()
            reward.type = 5
            reward.lv = 1
            reward.itemname = "宝石"
            reward.num = 0
            if isinstance(result.m_objResult["baoshi"], list):
                for baoshi in result.m_objResult["baoshi"]:
                    reward.num += int(baoshi["num"])
            else:
                reward.num += int(result.m_objResult["baoshi"]["num"])
            reward_info = RewardInfo()
            reward_info.m_listRewards.append(reward)
            self.add_reward(reward_info)
            self.info("打开{}个锦囊，获得{}".format(num, reward_info))
