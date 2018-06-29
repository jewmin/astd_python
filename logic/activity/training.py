# -*- coding: utf-8 -*-
# 大练兵
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class Training(ActivityTask):
    def __init__(self):
        super(Training, self).__init__(ActivityType.TrainingEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "大练兵"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_info()
        if info is None:
            return self.next_half_hour()

        if info["状态"] == 0:
            self.start()
            return self.immediate()

        if info["第几轮"] > 0:
            army_idx = -1
            max_army = -1
            for idx, army in enumerate(info["部队"], 1):
                if int(army) > max_army:
                    army_idx = idx
                    max_army = int(army)
            self.attack_army(army_idx, max_army)
            return self.immediate()

        for idx, hongbao in enumerate(info["战旗"], 1):
            if hongbao == "1":
                self.rec_hongbao(idx)

        hongbao = 0
        while info["红包"] > 0:
            if hongbao >= 3 and info["免费重置奖励次数"] > 0:
                self.reset_reward()
                return self.immediate()

            self.get_reward()
            info["红包"] -= 1
            hongbao += 1

        return self.next_half_hour()

    def get_info(self):
        url = "/root/training!getInfo.action"
        result = self.get_xml(url, "大练兵")
        if result and result.m_bSucceed:
            info = dict()
            info["状态"] = int(result.m_objResult["training"]["trainingstate"])
            info["第几轮"] = int(result.m_objResult["training"]["round"])
            info["部队"] = result.m_objResult["training"]["aramy"]  # 111123
            info["战旗"] = result.m_objResult["training"]["flags"]  # 0000
            info["红包"] = int(result.m_objResult["training"]["hongbao"])
            info["免费重置奖励次数"] = int(result.m_objResult["training"]["resettime"])
            return info

    def start(self):
        url = "/root/training!start.action"
        result = self.get_xml(url, "开始大练兵")
        if result and result.m_bSucceed:
            self.info("开始大练兵")

    def attack_army(self, army_idx, army):
        army_tuple = ("", "普通", "精英", "首领")
        url = "/root/training!attackArmy.action"
        data = {"army": army_idx}
        result = self.post_xml(url, data, "攻击部队")
        if result and result.m_bSucceed:
            self.info("攻击[{}]部队，获得{}红包".format(army_tuple[army], result.m_objResult["addhongbao"]))

    def rec_hongbao(self, hongbao):
        url = "/root/training!recHongbao.action"
        data = {"hongbao": hongbao}
        result = self.post_xml(url, data, "领取战旗奖励")
        if result and result.m_bSucceed:
            self.info("领取战旗奖励，获得{}红包".format(result.m_objResult["addhongbao"]))

    def reset_reward(self):
        url = "/root/training!resetReward.action"
        result = self.get_xml(url, "重置奖励")
        if result and result.m_bSucceed:
            self.info("重置大练兵奖励")

    def get_reward(self):
        url = "/root/training!getReward.action"
        result = self.get_xml(url, "打开红包")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("打开红包，获得{}".format(reward_info))
