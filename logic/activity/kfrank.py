# -*- coding: utf-8 -*-
# 对战
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType


class KFRank(ActivityTask):
    def __init__(self):
        super(KFRank, self).__init__(ActivityType.KfRank)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "对战"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.m_ActivityMgr.get_match_detail()
        if info is None:
            return self.next_half_hour()

        while info["拥有宝箱"] > 0:
            self.m_ActivityMgr.open_box()
            info["拥有宝箱"] -= 1

        if info["任务"]["state"] == "1":
            self.m_ActivityMgr.recv_task_reward()

        if info["可领取上届排名奖励"]:
            self.m_ActivityMgr.recv_last_reward()

        if self.m_dictConfig["task"]["enable"]:
            while info["任务"] is not None and info["任务"]["name"] not in self.m_dictConfig["task"]["list"]:
                info["任务"] = self.m_ActivityMgr.change_task()

        if info["准备状态"]:
            general_mgr = self.m_objServiceFactory.get_general_mgr()
            old_formation = general_mgr.formation()
            new_formation = self.m_dictConfig["ack_formation"] if info["对战可领取宝箱"] else self.m_dictConfig[
                "def_formation"]
            general_mgr.save_default_formation(new_formation)
            self.m_ActivityMgr.sync_data()
            self.m_ActivityMgr.ready()
            general_mgr.save_default_formation(old_formation)
            return info["下次战斗冷却时间"]
        elif info["状态"] == "2":
            return self.next_half_hour()
        elif info["对战状态"] == "2":
            return self.one_minute()
        elif info["对战状态"] == "1":
            return self.immediate() * 5
        elif info["花费军令"] > self.m_dictConfig["limit_token"]:
            return self.next_day(8)
        else:
            if info["对战可领取宝箱"] or not self.is_finish_task(21) or (self.m_dictConfig["def_enable"] and info["积分"] > self.m_dictConfig["def_score"]):
                self.m_ActivityMgr.start_match(info["花费军令"])
                return self.immediate()
            else:
                return self.next_half_hour()
