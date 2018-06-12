# -*- coding: utf-8 -*-
# 大宴群雄
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class BGEvent(ActivityTask):
    def __init__(self):
        super(BGEvent, self).__init__(ActivityType.BGEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "大宴群雄"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_bg_event_info()
        if info is None:
            return self.next_half_hour()

        for progress_state in info["宴请奖励"]:
            if progress_state["state"] == "1":
                self.get_banquet_reward(progress_state)

        if info["花费金币"] <= self.m_dictConfig["limit_cost"]:
            self.do_bg_event(info["花费金币"])
            return self.immediate()

        return self.next_half_hour()

    def get_bg_event_info(self):
        url = "/root/event!getBGEventInfo.action"
        result = self.m_objProtocolMgr.get_xml(url, "大宴群雄")
        if result and result.m_bSucceed:
            info = dict()
            info["花费金币"] = int(result.m_objResult["goldcost"])
            info["宴请奖励"] = result.m_objResult["progressstate"]
            return info

    def get_banquet_reward(self, progress_state):
        url = "/root/event!getBanquetReward.action"
        data = {"rewardId": progress_state["id"]}
        result = self.m_objProtocolMgr.post_xml(url, data, "开启宴请宝箱")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("开启宴请宝箱，获得{}".format(reward_info))

    def do_bg_event(self, cost):
        url = "/root/event!doBGEvent.action"
        result = self.m_objProtocolMgr.get_xml(url, "宴请群雄")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["bginfo"]["rewardinfo"])
            if cost > 0:
                self.info("花费{}金币宴请群雄，获得{}".format(cost, reward_info), True)
            else:
                self.info("免费宴请群雄，获得{}".format(reward_info))
