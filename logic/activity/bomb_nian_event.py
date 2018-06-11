# -*- coding: utf-8 -*-
# 抓年兽
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class BombNianEvent(ActivityTask):
    def __init__(self):
        super(BombNianEvent, self).__init__(ActivityType.BombNianEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "抓年兽"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_bomb_nian_info()
        if info is None:
            return self.next_half_hour()

        if info["领奖状态"] == 1:
            info["奖励"] = sorted(info["奖励"], key=lambda reward: self.m_dictConfig["reward_index"].get(reward["rewardinfo"]["reward"]["type"], 99))
            for reward_info in info["奖励"]:
                if reward_info["state"] == "1":
                    self.open_gift(reward_info["id"])
            return self.immediate()

        self.info("年兽血量：{}/{}".format(info["年兽血量"], info["年兽最大血量"]))
        for idx, hp in enumerate(self.m_dictConfig["hp"]):
            if info["年兽血量"] >= hp:
                info["鞭炮"] = sorted(info["鞭炮"], key=lambda obj: self.m_dictConfig["bomb"][idx][obj["类型"]])
                for bomb in info["鞭炮"]:
                    if bomb["免费次数"] > 0 or bomb["花费金币"] <= self.m_dictConfig["gold"][bomb["类型"]]:
                        self.bomb_nian(bomb)
                        return self.immediate()

        self.hunt_nian()

        return self.next_half_hour()

    def get_bomb_nian_info(self):
        url = "/root/bombNianEvent!getBombNianInfo.action"
        result = self.get_xml(url, "抓年兽")
        if result and result.m_bSucceed:
            info = dict()
            info["年兽血量"] = int(result.m_objResult["playerbombnianeventinfo"]["nianhp"])
            info["年兽最大血量"] = int(result.m_objResult["playerbombnianeventinfo"]["nianmaxhp"])
            info["鞭炮"] = list()
            info["鞭炮"].append({
                "类型": 1,
                "免费次数": int(result.m_objResult["playerbombnianeventinfo"]["firecrackersnum"]),
                "花费金币": int(result.m_objResult["playerbombnianeventinfo"]["firecrackerscost"]),
            })
            info["鞭炮"].append({
                "类型": 2,
                "免费次数": int(result.m_objResult["playerbombnianeventinfo"]["stringfirecrackersnum"]),
                "花费金币": int(result.m_objResult["playerbombnianeventinfo"]["stringfirecrackerscost"]),
            })
            info["鞭炮"].append({
                "类型": 3,
                "免费次数": int(result.m_objResult["playerbombnianeventinfo"]["springthundernum"]),
                "花费金币": int(result.m_objResult["playerbombnianeventinfo"]["springthundercost"]),
            })
            info["领奖状态"] = int(result.m_objResult["canget"])
            info["奖励"] = result.m_objResult["reward"]
            return info

    def open_gift(self, gift_id):
        url = "/root/bombNianEvent!openGift.action"
        data = {"giftId": gift_id}
        result = self.post_xml(url, data, "捡起奖励")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("捡起奖励，获得{}".format(reward_info))

    def bomb_nian(self, bomb):
        url = "/root/bombNianEvent!bombNian.action"
        data = {"bombType": bomb["类型"]}
        result = self.post_xml(url, data, "放鞭炮")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["bombnianreward"]["rewardinfo"])
            self.add_reward(reward_info)
            if bomb["免费次数"] > 0:
                self.info("免费放鞭炮，获得{}".format(reward_info))
            else:
                self.consume_gold(bomb["花费金币"])
                self.info("花费{}金币放鞭炮，获得{}".format(bomb["花费金币"], reward_info), True)

    def hunt_nian(self):
        url = "/root/bombNianEvent!huntNian.action"
        result = self.get_xml(url, "捕抓年兽")
        if result and result.m_bSucceed:
            if result.m_objResult.get("huntstate", "0") == "1":
                reward_info = RewardInfo()
                reward_info.handle_info(result.m_objResult["huntnianreward"]["rewardinfo"])
                self.add_reward(reward_info)
                self.info("捕抓年兽成功，获得{}".format(reward_info))
            else:
                self.info("捕抓年兽失败")
