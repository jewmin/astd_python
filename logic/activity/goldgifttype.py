# -*- coding: utf-8 -*-
# 盛宴活动
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo, Reward


class GoldGiftType(ActivityTask):
    def __init__(self):
        super(GoldGiftType, self).__init__(ActivityType.GoldGiftType)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "盛宴活动"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.kf_banquet()
        if info is None:
            return self.next_half_hour()

        if info["基础点券"] > 0:
            self.choosen_double(0, info["再喝一杯花费金币"], info["基础点券"])
            return self.immediate()
        elif info["所在房间"] > 0:
            return self.immediate() * 5
        elif info["状态"] == 1:
            if info["加入盛宴免费次数"] > 0:
                for room in info["盛宴房间"]:
                    if int(room["bufnum"]) > 0 and int(room["nation"]) == self.m_objUser.m_nNation:
                        self.join_banquet(room)
                        return self.immediate()
            elif info["加入盛宴花费金币"] <= self.m_dictConfig["buyjoingold"] and info["加入盛宴花费金币"] <= self.get_available_gold():
                self.buy_banquet_num(1, info["加入盛宴花费金币"])
                return self.immediate()

        return self.next_half_hour()

    def kf_banquet(self):
        url = "/root/kfBanquet.action"
        result = self.get_xml(url, "盛宴活动")
        if result and result.m_bSucceed:
            info = dict()
            info["加入盛宴免费次数"] = int(result.m_objResult.get("canjoinnum", "0"))
            info["加入盛宴花费金币"] = int(result.m_objResult.get("buyjoingold", "0"))
            info["盛宴房间"] = result.m_objResult["room"]
            info["基础点券"] = int(result.m_objResult.get("basedoubletickets", "0"))
            info["再喝一杯花费金币"] = int(result.m_objResult.get("doublegold", "0"))
            info["所在房间"] = int(result.m_objResult.get("inroomrank", "0"))
            info["状态"] = int(result.m_objResult["status"])
            return info

    def join_banquet(self, room):
        url = "/root/kfBanquet!joinBanquet.action"
        data = {"room": room["rank"]}
        result = self.post_xml(url, data, "加入盛宴")
        if result and result.m_bSucceed:
            self.info("参加第{}名[{}]的盛宴".format(room["rank"], room["playername"]))

    def buy_banquet_num(self, num, cost):
        url = "/root/kfBanquet!buyBanquetNum.action"
        data = {"num": num}
        result = self.post_xml(url, data, "购买邀请券")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            self.info("花费{}金币，购买{}张邀请券".format(cost, num))

    def choosen_double(self, double, cost, base_tickets):
        url = "/root/kfBanquet!choosenDouble.action"
        data = {"type": double}
        result = self.post_xml(url, data, "再喝一杯")
        if result and result.m_bSucceed:
            reward = Reward()
            reward.type = 42
            reward.num = base_tickets
            reward.itemname = "点券"
            reward.lv = 1
            if double == 1:
                self.consume_gold(cost)
                reward.num += int(result.m_objResult["tickets"])
                msg = "花费{}金币，再喝一杯"
            else:
                msg = "不胜酒力"
            reward_info = RewardInfo()
            reward_info.m_listRewards.append(reward)
            self.add_reward(reward_info)
            msg += "，获得{}".format(reward_info)
            self.info(msg, double == 1)
