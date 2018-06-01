# -*- coding: utf-8 -*-
# 征战管理
from manager.base_mgr import BaseMgr
from model.reward_info import RewardInfo


class BattleMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(BattleMgr, self).__init__(time_mgr, service_factory, user, index)

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
