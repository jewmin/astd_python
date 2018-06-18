# -*- coding: utf-8 -*-
# 武斗庆典
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType


class KFEvent(ActivityTask):
    def __init__(self):
        super(KFEvent, self).__init__(ActivityType.KfWDEventReward)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "武斗庆典"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_kfwd_event_info()
        if info is None:
            return self.next_half_hour()

        if info["奖励"] > 0:
            self.get_kfwd_reward()

        return self.next_half_hour()

    def get_kfwd_event_info(self):
        url = "/root/kfEvent!getKfwdEventInfo.action"
        result = self.get_xml(url, "武斗庆典")
        if result and result.m_bSucceed:
            info = dict()
            info["奖励"] = int(result.m_objResult.get("rewardgold", "0"))
            return info

    def get_kfwd_reward(self):
        url = "/root/kfEvent!getKfwdReward.action"
        result = self.get_xml(url, "武斗庆典奖励")
        if result and result.m_bSucceed:
            self.info("领取武斗庆典奖励，获得{}宝箱".format(result.m_objResult["tickets"]))
