# -*- coding: utf-8 -*-
# 武斗庆典
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo, Reward


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

        info = self.getKfwdEventOtherInfo()
        if info is None:
            return self.next_half_hour()

        while info["奖励"] > 0:
            info["奖励"] -= 1
            self.open_box_by_id(0)

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

    def getKfwdEventOtherInfo(self):
        url = "/root/kfEvent!getKfwdEventOtherInfo.action"
        result = self.get_xml(url, "武斗会龙虎榜")
        if result and result.m_bSucceed:
            info = dict()
            info["奖励"] = int(result.m_objResult.get("playerboxinfo", {}).get("boxnum", "0"))
            return info

    def open_box_by_id(self, gold_type):
        url = "/root/kfwd!openBoxById.action"
        data = {"gold": gold_type}
        result = self.post_xml(url, data, "开启武斗会龙虎榜宝箱")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["message"]["rewardinfo"])
            reward = Reward()
            reward.type = 42
            reward.num = int(result.m_objResult["message"]["tickets"])
            reward.itemname = "点券"
            reward.lv = 1
            reward_info.m_listRewards.append(reward)
            self.add_reward(reward_info)
            self.info("开启武斗会龙虎榜宝箱，获得{}".format(reward_info))
