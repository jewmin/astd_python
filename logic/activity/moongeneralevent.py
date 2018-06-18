# -*- coding: utf-8 -*-
# 赏月送礼
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo, Reward


class MoonGeneralEvent(ActivityTask):
    def __init__(self):
        super(MoonGeneralEvent, self).__init__(ActivityType.MoonGeneralEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "赏月送礼"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_mg_event_info()
        if info is None:
            return self.next_half_hour()

        finish = True
        for idx, moralinfo in enumerate(info["士气奖励列表"], 1):
            if moralinfo["state"] == "0":
                finish = False
            elif moralinfo["state"] == "1":
                self.recv_moral_reward(idx)

        if not finish and info["送礼免费次数"] > 0:
            self.eat_moon_cake(info["武将"], 0)
            return self.immediate()
        elif not finish and info["送礼花费金币"] <= self.m_dictConfig["cakecost"] and info["送礼花费金币"] <= self.get_available_gold():
            self.eat_moon_cake(info["武将"], info["送礼花费金币"])
            return self.immediate()
        elif info["有下一位武将"]:
            self.next_general()
            return self.immediate()
        elif info["购买轮数花费金币"] <= self.m_dictConfig["buyroundcost"] and info["购买轮数花费金币"] <= self.get_available_gold():
            self.next_general()
            return self.immediate()

        return self.next_half_hour()

    def get_mg_event_info(self):
        url = "/root/event!getMGEventInfo.action"
        result = self.get_xml(url, "赏月送礼")
        if result and result.m_bSucceed:
            info = dict()
            info["免费轮数"] = int(result.m_objResult["freeround"])
            info["购买轮数花费金币"] = int(result.m_objResult["buyroundcost"])
            info["宝物领取状态"] = int(result.m_objResult["baowuget"])
            info["红宝领取状态"] = int(result.m_objResult["cangetbao"])
            info["送礼免费次数"] = int(result.m_objResult["gmginfo"]["freecakenum"])
            info["送礼花费金币"] = int(result.m_objResult["gmginfo"].get("cakecost", "0"))
            info["有下一位武将"] = result.m_objResult["gmginfo"].get("havenextg", "0") == "1"
            info["武将"] = result.m_objResult["gmginfo"]["name"]
            if isinstance(result.m_objResult["gmginfo"]["moralinfo"], list):
                info["士气奖励列表"] = result.m_objResult["gmginfo"]["moralinfo"]
            else:
                info["士气奖励列表"] = [result.m_objResult["gmginfo"]["moralinfo"]]
            return info

    def recv_moral_reward(self, idx):
        url = "/root/event!recvMoralReward.action"
        data = {"rewardId": idx}
        result = self.post_xml(url, data, "领取士气奖励")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("领取士气奖励，获得{}".format(reward_info))

    def eat_moon_cake(self, name, cost):
        url = "/root/event!eatMoonCake.action"
        result = self.get_xml(url, "吃月饼")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            if cost > 0:
                self.info("武将[{}]：花费{}金币，吃月饼".format(name, cost), True)
            else:
                self.info("武将[{}]：免费吃月饼".format(name))

    def next_general(self):
        url = "/root/event!nextGeneral.action"
        result = self.get_xml(url, "下一位")
        if result and result.m_bSucceed:
            self.info("下一位武将[{}]".format(result.m_objResult["gmginfo"]["name"]))
