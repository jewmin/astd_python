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

        war_beast_config = config["equip"]["war_beast"]
        if war_beast_config["enable"]:
            dict_info = self.getInfoList()
            if dict_info:
                if dict_info["精魄"] > 0:
                    for war_beast in dict_info["已有战兽"]:
                        while war_beast and int(war_beast["exp"]) < int(war_beast["upexp"]) and dict_info["精魄"] > 0:
                            war_beast = self.feed(war_beast["warbeastid"], 1)
                            dict_info["精魄"] -= 1

                if dict_info["高级精魄"] > 0:
                    for war_beast in dict_info["已有战兽"]:
                        while war_beast and int(war_beast["exp"]) < int(war_beast["upexp"]) and dict_info["高级精魄"] > 0:
                            war_beast = self.feed(war_beast["warbeastid"], 2)
                            dict_info["高级精魄"] -= 1

        return self.next_half_hour()

    def get_war_beast_temple(self):
        url = "/root/warbeastTemple!getInfo.action"
        result = self.m_objProtocolMgr.get_xml(url, "战兽圣殿")
        if result and result.m_bSucceed:
            dict_info = {}
            dict_info["购买1次"] = int(
                result.m_objResult["warbeasttemple"]["buyonecost"])
            dict_info["购买10次"] = int(
                result.m_objResult["warbeasttemple"]["buytencost"])
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
            self.m_objServiceFactory.get_equip_mgr().info(
                "{}，获得{}".format(msg, reward_info), use_gold)
            return True

    def getInfoList(self):
        url = "/root/warbeast!getInfoList.action"
        result = self.m_objProtocolMgr.get_xml(url, "战兽")
        if result and result.m_bSucceed:
            dict_info = {
                "战兽列表": result.m_objResult["warbeastlist"]["warbeast"],
                "已有战兽": result.m_objResult["warbeast"],
                "精魄": int(result.m_objResult.get("food1", 0)),
                "高级精魄": int(result.m_objResult.get("food2", 0)),
            }
            if not isinstance(dict_info["战兽列表"], list):
                dict_info["战兽列表"] = [dict_info["战兽列表"]]
            if not isinstance(dict_info["已有战兽"], list):
                dict_info["已有战兽"] = [dict_info["已有战兽"]]
            return dict_info

    def feed(self, warbeastId, foodType):
        url = "/root/warbeast!feed.action"
        data = {"warbeastId": int(warbeastId), "foodType": foodType}
        result = self.m_objProtocolMgr.post_xml(url, data, "喂养战兽")
        if result and result.m_bSucceed:
            warbeast = result.m_objResult["warbeast"]
            self.m_objServiceFactory.m_objMiscMgr.info("喂养战兽[{}], 当前进度({}/{})".format(warbeast["warbeastid"], warbeast["exp"], warbeast["upexp"]))
            return warbeast
