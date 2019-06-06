# -*- coding: utf-8 -*-
# 龙舟
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class BoatEvent(ActivityTask):
    def __init__(self):
        super(BoatEvent, self).__init__(ActivityType.BoatEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "龙舟"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_boat_event_info()
        if info is None:
            return self.next_half_hour()

        if info["组队中"] == 1:
            return self.immediate()

        if info["阶段"] == 2:
            self.start_boat_comp()
            return self.immediate()

        if info["阶段"] == 3:
            if info["冲刺花费金币"] <= self.m_dictConfig["gold"]:
                self.dash_boat_event(info["冲刺花费金币"])
            return self.immediate()

        if info["阶段"] == 4:
            if info["奖励状态"] == 0:
                self.recv_boat_event_final_reward()
                return self.immediate()
            else:
                return self.next_half_hour()

        if info["剩余次数"] > 0:
            for team in info["队伍列表"]:
                if int(team["quality"]) == info["龙舟品质"]:
                    self.join_boat_event_team(team["teamid"])
                    return self.immediate()
            if self.m_dictConfig["create"]:
                self.creat_boat_event_team()
            return self.immediate()

        self.sign_up_boat_event()
        return self.immediate()

    def get_boat_event_info(self):
        url = "/root/event!getBoatEventInfo.action"
        data = {"notice": 0}
        result = self.m_objProtocolMgr.post_xml(url, data, "获取龙舟信息")
        if result and result.m_bSucceed:
            info = dict()
            info["组队中"] = int(result.m_objResult.get("inteam", "0"))
            info["阶段"] = int(result.m_objResult.get("stage", "0"))
            info["冲刺花费金币"] = int(result.m_objResult.get("dashcost", "100"))
            info["奖励状态"] = int(result.m_objResult.get("signreward", {}).get("state", "0"))
            info["剩余次数"] = int(result.m_objResult.get("playerboat", {}).get("remaintimes", "0"))
            info["龙舟品质"] = int(result.m_objResult.get("playerboat", {}).get("quality", "0"))
            team_list = result.m_objResult.get("team", [])
            if not isinstance(team_list, list):
                team_list = [team_list]
            info["队伍列表"] = team_list # quality teamid
            return info

    def upgrade_boat(self, cost):
        url = "/root/event!upgradeBoat.action"
        result = self.m_objProtocolMgr.get_xml(url, "升级龙舟")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            self.info("花费{}金币，升级龙舟".format(cost))

    def join_boat_event_team(self, team_id):
        url = "/root/event!joinBoatEventTeam.action"
        data = {"teamId": team_id}
        result = self.m_objProtocolMgr.post_xml(url, data, "加入龙舟队伍")
        if result and result.m_bSucceed:
            self.info("加入龙舟队伍[{}]".format(team_id))

    def creat_boat_event_team(self):
        url = "/root/event!creatBoatEventTeam.action"
        result = self.m_objProtocolMgr.get_xml(url, "创建龙舟队伍")
        if result and result.m_bSucceed:
            self.info("创建龙舟队伍")

    def sign_up_boat_event(self):
        url = "/root/event!signUpBoatEvent.action"
        data = {"signUpId": 0}
        result = self.m_objProtocolMgr.post_xml(url, data, "报名龙舟大赛")
        if result and result.m_bSucceed:
            self.info("报名龙舟大赛")

    def start_boat_comp(self):
        url = "/root/event!startBoatComp.action"
        result = self.m_objProtocolMgr.get_xml(url, "开始龙舟大赛")
        if result and result.m_bSucceed:
            self.info("开始龙舟大赛")

    def dash_boat_event(self, cost):
        url = "/root/event!dashBoatEvent.action"
        result = self.m_objProtocolMgr.get_xml(url, "龙舟冲刺")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            if cost > 0:
                self.info("花费{}金币龙舟冲刺".format(cost), True)
            else:
                self.info("免费龙舟冲刺")

    def recv_boat_event_final_reward(self):
        url = "/root/event!recvBoatEventFinalReward.action"
        result = self.m_objProtocolMgr.get_xml(url, "领取龙舟大赛奖励")
        if result and result.m_bSucceed:
            msg = "领取龙舟大赛奖励，获得"
            if "signreward" in result.m_objResult:
                reward_info = RewardInfo()
                reward_info.handle_info(result.m_objResult["signreward"]["rewardinfo"])
                self.add_reward(reward_info)
                msg += "冲刺奖励{} ".format(reward_info)
            if "rankreward" in result.m_objResult:
                reward_info = RewardInfo()
                reward_info.handle_info(result.m_objResult["rankreward"]["rewardinfo"])
                self.add_reward(reward_info)
                msg += "排名奖励{} ".format(reward_info)
            if "milesreward" in result.m_objResult:
                reward_info = RewardInfo()
                reward_info.handle_info(result.m_objResult["milesreward"]["rewardinfo"])
                self.add_reward(reward_info)
                msg += "路程奖励{} ".format(reward_info)
            self.info(msg)
