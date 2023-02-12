# -*- coding: utf-8 -*-
# 战兽圣殿任务
from logic.base_task import BaseTask
from logic.config import config
from model.reward_info import RewardInfo


class WarbeastTempleTask(BaseTask):
    def __init__(self):
        super(WarbeastTempleTask, self).__init__()
        self.m_szName = "war_beast_temple"
        self.m_szReadable = "战兽圣殿"

    def run(self):
        war_beast_temple_config = config["equip"]["war_beast_temple"]
        if war_beast_temple_config["enable"]:
            dict_info = self.get_war_beast_temple()
            if dict_info is not None:
                if dict_info["购买1次"] <= war_beast_temple_config["gold"]:
                    success = self.buy_war_beast(1, dict_info["购买1次"])
                    if success:
                        return self.immediate()
                    else:
                        return self.next_half_hour()

        return self.next_half_hour()

    def get_war_beast_temple(self):
        url = "/root/warbeastTemple!getInfo.action"
        result = self.m_objProtocolMgr.get_xml(url, "战兽圣殿")
        if result and result.m_bSucceed:
            dict_info = {}
            dict_info["购买1次"] = int(result.m_objResult["warbeasttemple"]["buyonecost"])
            dict_info["购买10次"] = int(result.m_objResult["warbeasttemple"]["buytencost"])
            return dict_info

    def buy_war_beast(self, typ, cost):
        url = "/root/warbeastTemple!buy.action"
        data = {"type": typ}
        result = self.m_objProtocolMgr.post_xml(url, data, "购买")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            if cost > 0:
                msg = "花费{}金币购买".format(cost)
                use_gold = True
            else:
                msg = "免费购买"
                use_gold = False
            self.m_objServiceFactory.get_equip_mgr().info("{}，获得{}".format(msg, reward_info), use_gold)
            return True
