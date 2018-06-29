# -*- coding: utf-8 -*-
# 英雄帖
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo, Reward


class KfPVP(ActivityTask):
    def __init__(self):
        super(KfPVP, self).__init__(ActivityType.ShowKfPVP)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "英雄帖"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_signup_list()
        if info is None:
            return self.next_half_hour()

        if info["报名状态"] == 0:
            self.sign_up()
            return self.immediate()
        elif info["报名状态"] == 1:
            detail = self.get_match_detail()
            if detail is not None:
                pass

        while info["宝箱"] > 0:
            info["宝箱"] -= 1
            self.open_box_by_id(0)

        return self.next_half_hour()

    def get_signup_list(self):
        url = "/root/kfpvp!getSignupList.action"
        result = self.get_xml(url, "英雄帖")
        if result and result.m_bSucceed:
            info = dict()
            info["报名状态"] = int(result.m_objResult["message"]["signupstate"])
            info["宝箱"] = int(result.m_objResult["message"]["playerboxinfo"]["boxnum"])
            info["冷却时间"] = int(result.m_objResult["message"]["cd"])
            info["免费鼓舞次数"] = int(result.m_objResult["message"]["freeinspire"])
            info["徽章"] = int(result.m_objResult["message"]["medalstate"])
            return info

    def sign_up(self):
        url = "/root/kfpvp!signUp.action"
        result = self.get_xml(url, "英雄帖报名")
        if result and result.m_bSucceed:
            self.info("英雄帖报名")

    def open_box_by_id(self, gold_type):
        url = "/root/kfpvp!openBoxById.action"
        data = {"gold": gold_type}
        result = self.post_xml(url, data, "开启英雄帖宝箱")
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
            self.info("开启英雄帖宝箱，获得{}".format(reward_info))

    def get_match_detail(self):
        url = "/root/kfpvp!getMatchDetail.action"
        result = self.get_xml(url, "英雄帖比赛详情")
        if result and result.m_bSucceed:
            detail = dict()
            detail["积分奖励"] = result.m_objResult["message"].get("scoreticketsreward", "0") == "1"
            return detail
    #
    # def get_score_tickets_reward(self):
    #     url = "/root/kfwd!getScoreTicketsReward.action"
    #     result = self.get_xml(url, "武斗会积分奖励")
    #     if result and result.m_bSucceed:
    #         self.info("武斗会积分奖励，获得{}宝箱".format(result.m_objResult["message"]["tickets"]))
    #
    # def get_tribute_detail(self):
    #     url = "/root/kfwd!getTributeDetail.action"
    #     result = self.get_xml(url, "武斗会结算详情")
    #     if result and result.m_bSucceed:
    #         detail = dict()
    #         detail["积分奖励"] = result.m_objResult["message"].get("scoreticketsreward", "0") == "1"
    #         detail["比赛奖励"] = result.m_objResult["message"]["tributeinfo"]["tributelist"]["tribute"]
    #         return detail
    #
    # def buy_tribute(self, tribute):
    #     url = "/root/kfwd!buyTribute.action"
    #     result = self.get_xml(url, "武斗会比赛奖励")
    #     if result and result.m_bSucceed:
    #         self.info("花费{}金币领取武斗会比赛奖励，获得{}宝箱".format(tribute.get("gold", "0"), tribute["tickets"]))
    #
    # def get_wd_medal_gift(self):
    #     url = "/root/kfwd!getWdMedalGift.action"
    #     result = self.get_xml(url, "武斗会勋章")
    #     if result and result.m_bSucceed:
    #         info = dict()
    #         info["勋章"] = result.m_objResult["message"]["medal"]
    #         return info
    #
    # def recv_wd_medal_gift(self, medal):
    #     url = "/root/kfwd!recvWdMedalGift.action"
    #     data = {"medalId": medal["id"]}
    #     result = self.post_xml(url, data, "领取武斗会勋章奖励")
    #     if result and result.m_bSucceed:
    #         reward = Reward()
    #         reward.type = 5
    #         reward.lv = int(result.m_objResult["message"]["baoshi"]["baoshilevel"])
    #         reward.num = int(result.m_objResult["message"]["baoshi"]["baoshinum"])
    #         reward.itemname = "宝石"
    #         reward_info = RewardInfo()
    #         reward_info.m_listRewards.append(reward)
    #         self.add_reward(reward_info)
    #         self.info("领取武斗会勋章奖励，获得{}".format(reward_info))
