# -*- coding: utf-8 -*-
# 草船借箭
import random
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class BorrowingArrowsEvent(ActivityTask):
    def __init__(self):
        super(BorrowingArrowsEvent, self).__init__(ActivityType.BorrowingArrowsEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "草船借箭"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_player_borrowing_arrows_event_info()
        if info is None:
            return self.next_half_hour()

        self.info("草船借箭：军功({}/{})，钥匙({})，承重({}/{})".format(info["剩余军功"], info["总军功"], info["钥匙数量"], info["承重"], info["承重上限"]))
        info["宝箱"] = sorted(info["宝箱"], key=lambda obj: self.m_dictConfig["unlock"][obj["rewardtype"]])

        status = info["钥匙"].split(",")
        for idx, s in enumerate(status):
            if s == "0":
                self.get_key(idx)

        if info["钥匙数量"] > 0:
            for reward in info["宝箱"]:
                if reward["buynum"] == "-1":
                    self.unlock_reward(reward)
                    return self.immediate()

        for reward in info["宝箱"]:
            if reward["buynum"] != "-1":
                cost = int(reward["cost"])
                if cost <= self.m_dictConfig["cost_limit"] and cost <= info["剩余军功"]:
                    self.exchange_reward(reward)
                    return self.immediate()

        if info["状态"] == -2:
            if info["免费发船"] > 0:
                self.set_sail(0)
                return self.immediate()
            elif info["发船花费金币"] <= self.m_dictConfig["sail_gold"] and info["发船花费金币"] <= self.get_available_gold():
                self.set_sail(info["发船花费金币"])
                return self.immediate()
            else:
                return self.next_half_hour()
        elif info["承重上限"] - info["承重"] <= self.m_dictConfig["arrow_diff"]:
            self.deliver_arrows()
        else:
            self.choice_stream(random.randint(0, 2))

        return self.immediate()

    def get_player_borrowing_arrows_event_info(self):
        url = "/root/borrowingArrowsEvent!getPlayerBorrowingArrowsEventInfo.action"
        result = self.get_xml(url, "草船借箭")
        if result and result.m_bSucceed:
            info = dict()
            info["剩余军功"] = int(result.m_objResult["borrowingarrowseventinfo"]["arrowsleft"])
            info["总军功"] = int(result.m_objResult["borrowingarrowseventinfo"]["arrowstotal"])
            info["钥匙"] = result.m_objResult["borrowingarrowseventinfo"]["stagestatus"]
            info["钥匙数量"] = int(result.m_objResult["borrowingarrowseventinfo"]["unlocknum"])
            info["宝箱"] = result.m_objResult["borrowingarrowseventinfo"]["exchangereward"]
            info["状态"] = int(result.m_objResult["borrowingarrowseventinfo"]["currentstream"])
            info["免费发船"] = int(result.m_objResult["borrowingarrowseventinfo"]["boatnum"])
            info["发船花费金币"] = int(result.m_objResult["borrowingarrowseventinfo"]["buyboatcost"])
            info["承重"] = int(result.m_objResult["borrowingarrowseventinfo"]["arrowsboat"])
            info["承重上限"] = int(result.m_objResult["borrowingarrowseventinfo"]["boatcapacity"])
            return info

    def set_sail(self, cost):
        url = "/root/borrowingArrowsEvent!setSail.action"
        result = self.get_xml(url, "发船")
        if result and result.m_bSucceed:
            if cost > 0:
                self.consume_gold(cost)
                self.info("花费{}金币发船".format(cost), True)
            else:
                self.info("免费发船")

    def choice_stream(self, stream_id):
        choice_tuple = ("下游", "中游", "上游")
        url = "/root/borrowingArrowsEvent!choiceStream.action"
        data = {"streamId": stream_id}
        result = self.post_xml(url, data, "选择区域")
        if result and result.m_bSucceed:
            msg = "选择{}，承重+{}".format(choice_tuple[stream_id], result.m_objResult["borrowingarrows"]["arrowsstream"])
            if result.m_objResult["borrowingarrows"]["borrowingresult"] == "0":
                msg += "，超重"
            self.info(msg)

    def deliver_arrows(self):
        url = "/root/borrowingArrowsEvent!deliverArrows.action"
        result = self.get_xml(url, "返航")
        if result and result.m_bSucceed:
            self.info("返航")

    def get_key(self, key_id):
        url = "/root/borrowingArrowsEvent!getKey.action"
        data = {"keyId": key_id}
        result = self.post_xml(url, data, "领取钥匙")
        if result and result.m_bSucceed:
            self.info("领取钥匙")

    def unlock_reward(self, reward):
        reward_tuple = ("镔铁", "点卷", "宝物", "宝石")
        url = "/root/borrowingArrowsEvent!unlockReward.action"
        data = {"rewardType": reward["rewardtype"]}
        result = self.post_xml(url, data, "开启宝箱")
        if result and result.m_bSucceed:
            self.info("开启[{}]宝箱".format(reward_tuple[int(reward["rewardtype"])]))

    def exchange_reward(self, reward):
        url = "/root/borrowingArrowsEvent!exchangeReward.action"
        data = {"rewardType": reward["rewardtype"]}
        result = self.post_xml(url, data, "邀功")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("花费{}军功，邀功，获得{}".format(reward["cost"], reward_info))
