# -*- coding: utf-8 -*-
# 武斗会
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class KfWD(ActivityTask):
    def __init__(self):
        super(KfWD, self).__init__(ActivityType.ShowKfWD)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "武斗会"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_signup_list()
        if info is None:
            return self.next_half_hour()

        if info["报名状态"] == 0:
            self.sign_up()
            return self.immediate()

        while info["宝箱"] > 0:
            info["宝箱"] -= 1
            self.open_box_by_id(0)

        return self.next_half_hour()

    def get_signup_list(self):
        url = "/root/kfwd!getSignupList.action"
        result = self.get_xml(url, "武斗会")
        if result and result.m_bSucceed:
            info = dict()
            info["报名状态"] = int(result.m_objResult["message"]["signupstate"])
            info["宝箱"] = int(result.m_objResult["message"]["playerboxinfo"]["boxnum"])
            return info

    def sign_up(self):
        url = "/root/kfwd!signUp.action"
        result = self.get_xml(url, "武斗会报名")
        if result and result.m_bSucceed:
            self.info("武斗会报名")

    def open_box_by_id(self, gold_type):
        url = "/root/kfwd!openBoxById.action"
        data = {"gold": gold_type}
        result = self.post_xml(url, data, "开启武斗会宝箱")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["message"]["rewardinfo"])
            self.add_reward(reward_info)
            self.info("开启武斗会宝箱，获得{}点券 {}".format(result.m_objResult["message"]["tickets"], reward_info))
