# -*- coding: utf-8 -*-
# 充值赠礼
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType


class GiftEvent(ActivityTask):
    def __init__(self):
        super(GiftEvent, self).__init__(ActivityType.NationDayGoldBoxEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "充值赠礼"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_gold_box_event_info()
        if info is None:
            return self.next_half_hour()

        if info["在线奖励"] == 1:
            self.recv_online_reward()
            return self.immediate()

        while info["宝箱"] > 0:
            info["宝箱"] -= 1
            self.open_gold_box_event()

        return self.next_half_hour()

    def get_gold_box_event_info(self):
        url = "/root/giftEvent!getGoldBoxEventInfo.action"
        result = self.get_xml(url, "充值赠礼")
        if result and result.m_bSucceed:
            info = dict()
            info["宝箱"] = int(result.m_objResult["boxnum"])
            info["在线奖励"] = int(result.m_objResult.get("onlinereward", "0"))
            return info

    def recv_online_reward(self):
        url = "/root/giftEvent!recvOnlineReward.action"
        result = self.get_xml(url, "领取在线奖励")
        if result and result.m_bSucceed:
            self.info("领取在线奖励，获得{}个宝箱".format(result.m_objResult["rewardbox"]))

    def open_gold_box_event(self):
        url = "/root/giftEvent!openGoldBoxEvent.action"
        result = self.get_xml(url, "开启充值赠礼宝箱")
        if result and result.m_bSucceed:
            if "baoshi" in result.m_objResult["reward"]:
                self.info("开启充值赠礼宝箱，获得{}宝石".format(result.m_objResult["reward"]["baoshi"]))
            elif "gold" in result.m_objResult["reward"]:
                self.info("开启充值赠礼宝箱，获得{}金币".format(result.m_objResult["reward"]["gold"]), True)
            elif "ticket" in result.m_objResult["reward"]:
                self.info("开启充值赠礼宝箱，获得{}点券".format(result.m_objResult["reward"]["ticket"]))
