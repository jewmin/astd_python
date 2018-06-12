# -*- coding: utf-8 -*-
# 抓捕活动
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class ArrestEvent(ActivityTask):
    def __init__(self):
        super(ArrestEvent, self).__init__(ActivityType.ArrestEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "抓捕活动"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_arrest_event_info()
        if info is None:
            return self.next_half_hour()

        if info["可领取抓捕令"] == 1:
            self.recv_arrest_token()
            return self.immediate()

        if info["俘虏"] > 0:
            if info["免费鞭子次数"] > 0:
                self.shen_slaves(True, 0)
            elif info["鞭子花费金币"] <= self.m_dictConfig["high_gold"]:
                self.shen_slaves(True, info["鞭子花费金币"])
            else:
                self.shen_slaves(False, 0)
            return self.immediate()

        if info["粽子数量"] > 0:
            self.eat_rice_dumpling()
            return self.immediate()

        if info["抓捕令"] == 0 and info["购买抓捕令花费金币"] <= self.m_dictConfig["buy_gold"]:
            self.buy_arrest_token(info["购买抓捕令花费金币"])
            return self.immediate()

        return self.next_half_hour()

    def get_arrest_event_info(self):
        url = "/root/event!getArrestEventInfo.action"
        result = self.get_xml(url, "抓捕活动")
        if result and result.m_bSucceed:
            info = dict()
            info["可领取抓捕令"] = int(result.m_objResult["cangettoken"])
            info["抓捕令"] = int(result.m_objResult["arresttokennum"])
            info["俘虏"] = int(result.m_objResult["slaves"])
            info["免费鞭子次数"] = int(result.m_objResult["freehighshen"])
            info["鞭子花费金币"] = int(result.m_objResult["hishengold"])
            info["粽子数量"] = int(result.m_objResult["ricedumpling"])
            info["购买抓捕令花费金币"] = int(result.m_objResult["arresttokencostgold"])

            return info

    def recv_arrest_token(self):
        url = "/root/event!recvArrestToken.action"
        result = self.get_xml(url, "抓捕活动")
        if result and result.m_bSucceed:
            self.info("领取{}抓捕令".format(result.m_objResult["arresttokennum"]))

    def shen_slaves(self, high, cost):
        url = "/root/event!shenSlaves.action"
        data = {"highLv": 1 if high else 0}
        result = self.post_xml(url, data, "审问俘虏")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.consume_gold(cost)
            self.info("{}审问俘虏，获得{}".format("使用鞭子，" if high else "", reward_info))

    def eat_rice_dumpling(self):
        url = "/root/event!eatRiceDumpling.action"
        result = self.get_xml(url, "享用端午密粽")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("享用端午密粽，获得{}".format(reward_info))

    def buy_arrest_token(self, cost):
        url = "/root/event!buyArrestToken.action"
        result = self.get_xml(url, "购买抓捕令")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            self.info("花费{}金币，购买抓捕令".format(cost))
