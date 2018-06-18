# -*- coding: utf-8 -*-
# 消费送礼
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo, Reward


class DoubleElevenEvent(ActivityTask):
    def __init__(self):
        super(DoubleElevenEvent, self).__init__(ActivityType.DoubleElevenEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "消费送礼"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_double_eleven_event_info()
        if info is None:
            return self.next_half_hour()

        for reward in info["奖励"]:
            if reward["state"] == "1":
                self.open_box(reward)

        while info["礼袋"] > 0:
            info["礼袋"] -= 1
            self.open_gift()

        return self.next_half_hour()

    def get_double_eleven_event_info(self):
        url = "/root/event!getDoubleElevenEventInfo.action"
        result = self.get_xml(url, "消费送礼")
        if result and result.m_bSucceed:
            info = dict()
            info["奖励"] = result.m_objResult["reward"]
            info["礼袋"] = int(result.m_objResult["giftnum"])
            return info

    def open_gift(self):
        url = "/root/event!openGift.action"
        result = self.get_xml(url, "打开礼袋")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("打开礼袋，获得{}".format(reward_info))

    def open_box(self, reward):
        url = "/root/event!openBox.action"
        data = {"boxNum": reward["id"]}
        result = self.post_xml(url, data, "打开消费累计宝箱")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("打开消费累计宝箱，获得{}".format(reward_info))
