# -*- coding: utf-8 -*-
# 征战管理
from manager.base_mgr import BaseMgr
from model.reward_info import RewardInfo


class BattleMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(BattleMgr, self).__init__(time_mgr, service_factory, user, index)
        self.m_szTeamId = None
        self.m_szArmiesId = None

    def battle(self):
        url = "/root/battle.action"
        result = self.get_protocol_mgr().get_xml(url, "征战")
        if result and result.m_bSucceed:
            info = dict()
            info["征战事件"] = result.m_objResult["battleevent"] if isinstance(result.m_objResult["battleevent"], dict) else {}
            info["免费强攻令"] = int(result.m_objResult.get("freeattnum", "0"))
            return info

    def battle_army(self, army_id, force=False):
        url = "/root/battle!forceBattleArmy.action" if force else "/root/battle!battleArmy.action"
        data = {"armyId": army_id}
        result = self.get_protocol_mgr().post_xml(url, data, "征战NPC")
        if result and result.m_bSucceed:
            self.info("{}NPC, {}, 你损失兵力{}, 敌方损失兵力{} ".format("强攻" if force else "征战", result.m_objResult["battlereport"]["message"], result.m_objResult["battlereport"]["attlost"], result.m_objResult["battlereport"]["deflost"]))

    def do_battle_event(self):
        url = "/root/battle!doBattleEvent.action"
        result = self.get_protocol_mgr().get_xml(url, "进行征战事件")
        if result and result.m_bSucceed:
            if "process" in result.m_objResult["battleevent"]:
                self.info("进行征战事件：{}".format(result.m_objResult["battleevent"]["process"]))
            else:
                self.info("进行征战事件：完毕")

    def recv_battle_event_reward(self):
        url = "/root/battle!recvBattleEventReward.action"
        result = self.get_protocol_mgr().get_xml(url, "领取征战事件奖励")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("领取征战事件奖励，获得{}".format(reward_info))

    def join_team(self, team_id):
        url = "/root/multiBattle!joinTeam.action"
        data = {"teamId": team_id}
        result = self.get_protocol_mgr().post_xml(url, data, "加入征战军团")
        if result and result.m_bSucceed:
            self.info("加入征战军团({})".format(team_id))

    def get_team_info(self, armies_id):
        url = "/root/multiBattle!getTeamInfo.action"
        data = {"armiesId": armies_id}
        result = self.get_protocol_mgr().post_xml(url, data, "征战军团")
        if result and result.m_bSucceed:
            if "team" in result.m_objResult:
                if isinstance(result.m_objResult["team"], list):
                    team = result.m_objResult["team"][0]
                else:
                    team = result.m_objResult["team"]
                self.join_team(team["teamid"])
                self.m_szArmiesId = armies_id
                self.m_szTeamId = team["teamid"]
            else:
                self.m_szTeamId = None
                self.m_szArmiesId = None
        else:
            self.m_szTeamId = None
            self.m_szArmiesId = None

    def get_power_info(self, power_id):
        url = "/root/battle!getPowerInfo.action"
        data = {"powerId": power_id}
        result = self.get_protocol_mgr().post_xml(url, data, "征战地图")
        if result and result.m_bSucceed:
            army_list = result.m_objResult["army"]
            return army_list
        else:
            return []

    def reset_soldier(self, general_id, force_num):
        url = "/root/mainCity!resetSoldier.action"
        data = {"generalId": general_id, "forceNum": force_num}
        result = self.get_protocol_mgr().post_xml(url, data, "设置残兵")
        if result and result.m_bSucceed:
            self.info("把武将[墨子]的兵力设置为{}".format(force_num))
