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
                me = detail["攻方"] if detail["攻方"]["playername"] == self.m_objUser.m_szUserName else detail["守方"]
                if detail["可以鼓舞"] and detail["免费鼓舞"] > 0 and me["inspire"]["attack"] == "0" and me["inspire"]["defend"] == "0":
                    self.inspire()
                    return self.immediate()
                elif detail["冷却时间"] > 0:
                    return detail["冷却时间"]
            elif info["冷却时间"] < 0:
                detail = self.get_tribute_detail()
                if detail is not None:
                    self.info("英雄帖初始排名：{}，最终排名：{}".format(detail["初始排名"], detail["最终排名"]))
                    if detail["最终排名奖励"]:
                        self.recv_reward_by_id(False)
                        return self.immediate()
                    if detail["最终排名前三奖励"]:
                        self.recv_reward_by_id(True)
                        return self.immediate()
                    if detail["徽章"] == 0:
                        self.recv_wd_medal()
                        return self.immediate()

        while info["宝箱"] > 0:
            info["宝箱"] -= 1
            self.open_box_by_id(0)

        return self.two_minute()

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
            detail["免费鼓舞"] = int(result.m_objResult["message"].get("freeinspire", "0"))
            detail["可以鼓舞"] = result.m_objResult["message"].get("caninspire", "0") == "1"
            detail["冷却时间"] = int(result.m_objResult["message"].get("cd", "0"))
            detail["攻方"] = result.m_objResult["message"]["attacker"]
            detail["守方"] = result.m_objResult["message"]["defender"]
            return detail

    def inspire(self):
        url = "/root/kfpvp!inspire.action"
        data = {"count": 1}
        result = self.post_xml(url, data, "跨服PVP鼓舞")
        if result and result.m_bSucceed:
            self.info("跨服PVP鼓舞")

    def get_tribute_detail(self):
        url = "/root/kfpvp!getTributeDetail.action"
        result = self.get_xml(url, "英雄帖结算详情")
        if result and result.m_bSucceed:
            detail = dict()
            detail["初始排名"] = int(result.m_objResult["message"]["expectrank"])
            detail["最终排名"] = int(result.m_objResult["message"]["finalrank"])
            detail["最终排名奖励"] = result.m_objResult["message"].get("cangetfinalreward", "0") == "1"
            detail["最终排名前三奖励"] = result.m_objResult["message"].get("cangettopreward", "0") == "1"
            detail["徽章"] = int(result.m_objResult["message"]["medalstate"])
            return detail

    def recv_reward_by_id(self, top3):
        url = "/root/kfpvp!recvRewardById.action"
        data = {"rewardId": 2 if top3 else 1}
        result = self.post_xml(url, data, "英雄帖最终排名奖励")
        if result and result.m_bSucceed:
            self.info("领取英雄帖最终排名奖励，获得{}宝箱".format(result.m_objResult["message"]["rewardbox"]))

    def recv_wd_medal(self):
        url = "/root/kfpvp!recvWdMedal.action"
        result = self.get_xml(url, "领取英雄帖勋章奖励")
        if result and result.m_bSucceed:
            self.info("领取英雄帖勋章奖励，获得{}".format(result.m_objResult["message"]["wdmedalname"]))
