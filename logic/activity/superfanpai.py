# -*- coding: utf-8 -*-
# 超级翻牌
import random
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo, Reward


class SuperFanPai(ActivityTask):
    def __init__(self):
        super(SuperFanPai, self).__init__(ActivityType.SuperFanPai)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "超级翻牌"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_super_fanpai_info()
        if info is None:
            return self.next_half_hour()

        if info["翻牌"]:
            self.fan_one(random.randint(1, 3))
            return self.immediate()
        else:
            tips = "卡牌："
            for card in info["卡牌"]:
                tips += "宝石lv.{}+{} ".format(card["gemlevel"], card["gemnumber"])
            self.info(tips)

            if info["翻牌次数"] > 0:
                buy_all = False
                info["卡牌"] = sorted(info["卡牌"], key=lambda obj: obj["gemlevel"])
                if info["卡牌"][0]["gemlevel"] >= self.m_dictConfig["superlv"]:
                    buy_all = True
                if buy_all and info["卡牌全开花费金币"] <= self.m_dictConfig["buyall"] and info["卡牌全开花费金币"] <= self.get_available_gold():
                    self.get_all(info["卡牌全开花费金币"])
                    return self.immediate()
                else:
                    self.xi_pai()
                    self.fan_one(info["卡牌"][-1]["id"])
                    return self.immediate()
            elif info["购买次数花费金币"] <= self.m_dictConfig["buyone"] and info["购买次数花费金币"] <= self.get_available_gold():
                self.buy_times(info["购买次数花费金币"])
                return self.immediate()

        return self.next_half_hour()

    def get_super_fanpai_info(self):
        url = "/root/superFanpai!getSuperFanpaiInfo.action"
        result = self.get_xml(url, "超级翻牌")
        if result and result.m_bSucceed:
            info = dict()
            info["购买次数花费金币"] = int(result.m_objResult["superfanpaiinfo"]["buyone"])
            info["卡牌全开花费金币"] = int(result.m_objResult["superfanpaiinfo"]["buyall"])
            info["翻牌次数"] = int(result.m_objResult["superfanpaiinfo"]["freetimes"])
            info["翻牌"] = result.m_objResult["superfanpaiinfo"].get("isfanpai", "0") == "1"
            if "card" in result.m_objResult["superfanpaiinfo"]:
                info["卡牌"] = result.m_objResult["superfanpaiinfo"]["card"]
                for idx, card in enumerate(info["卡牌"], 1):
                    card["id"] = idx
                    card["gemlevel"] = int(card["gemlevel"])
                    card["gemnumber"] = int(card["gemnumber"])
            return info

    def fan_one(self, card_id):
        url = "/root/superFanpai!fanOne.action"
        data = {"cardId": card_id}
        result = self.post_xml(url, data, "翻牌")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            for card in result.m_objResult["card"]:
                if card["ischoose"] == "1":
                    reward = Reward()
                    reward.type = 5
                    reward.lv = int(card["gemlevel"])
                    reward.num = int(card["gemnumber"])
                    reward.init()
                    reward_info.m_listRewards.append(reward)
                    break
            self.add_reward(reward_info)
            self.info("翻牌，获得{}".format(reward_info))

    def buy_times(self, cost):
        url = "/root/superFanpai!buyTimes.action"
        result = self.get_xml(url, "购买次数")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            self.info("花费{}金币，购买次数".format(cost), True)

    def get_all(self, cost):
        url = "/root/superFanpai!getAll.action"
        result = self.get_xml(url, "卡牌全开")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward = Reward()
            reward.type = 5
            reward.lv = 18
            reward.num = 3
            reward.init()
            reward_info.m_listRewards.append(reward)
            self.add_reward(reward_info)
            self.consume_gold(cost)
            self.info("花费{}金币，卡牌全开，获得{}".format(cost, reward_info), True)

    def xi_pai(self):
        url = "/root/superFanpai!xiPai.action"
        result = self.get_xml(url, "洗牌")
        if result and result.m_bSucceed:
            self.info("洗牌")
