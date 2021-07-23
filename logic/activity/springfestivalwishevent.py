# -*- coding: utf-8 -*-
# 许愿
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class SpringFestivalWishEvent(ActivityTask):
    def __init__(self):
        super(SpringFestivalWishEvent, self).__init__(ActivityType.SpringFestivalWishEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "许愿"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_spring_festival_wish_info()
        if info is None:
            return self.next_half_hour()

        if info["许愿状态"] == 1:  # 辞旧岁
            if info["下一福利"] is not None:
                reward_info = RewardInfo()
                reward_info.handle_info(info["下一福利"]["rewardinfo"])
                self.hang_in_the_tree(reward_info)
                return self.immediate()
            elif info["可领奖状态"] == 0:
                self.open_cijiu_reward()
                return self.immediate()
        elif info["许愿状态"] == 2:  # 迎新年
            if info["可领奖状态"] == 0:
                self.open_yinxing_reward()
                return self.immediate()
        elif info["许愿状态"] == 3:  # 领奖
            if info["愿望"] is not None:
                wishs = list(map(int, info["愿望"][:-1].split(",")))
                for idx, wish in enumerate(wishs, 1):
                    if wish == 0:
                        self.receive_wish_reward(idx)
                return self.immediate()

        return self.next_half_hour()

    def get_spring_festival_wish_info(self):
        url = "/root/springFestivalWish!getSpringFestivalWishInfo.action"
        result = self.get_xml(url, "许愿界面")
        if result and result.m_bSucceed:
            info = dict()
            info["许愿状态"] = int(result.m_objResult["nowevent"])
            info["下一福利"] = result.m_objResult.get("nextfu")
            info["可领奖状态"] = int(result.m_objResult.get("cangetreward", "0"))
            info["愿望"] = result.m_objResult.get("wishstate")
            return info

    def hang_in_the_tree(self, reward_info):
        url = "/root/springFestivalWish!hangInTheTree.action"
        result = self.get_xml(url, "挂许愿树")
        if result and result.m_bSucceed:
            self.info("挂许愿树，{}".format(reward_info))

    def open_cijiu_reward(self):
        url = "/root/springFestivalWish!openCijiuReward.action"
        result = self.get_xml(url, "辞旧岁")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("辞旧岁，获得{}".format(reward_info))

    def open_yinxing_reward(self):
        url = "/root/springFestivalWish!openYinxingReward.action"
        result = self.get_xml(url, "辞旧岁")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("迎新年，获得{}".format(reward_info))

    def receive_wish_reward(self, id):
        url = "/root/springFestivalWish!receiveWishReward.action"
        data = {"id": id}
        result = self.post_xml(url, data, "愿望")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("愿望，获得{}".format(reward_info))
