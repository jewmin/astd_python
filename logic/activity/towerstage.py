# -*- coding: utf-8 -*-
# 宝塔活动
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo, Reward
from model.global_func import GlobalFunc


class TowerStage(ActivityTask):
    def __init__(self):
        super(TowerStage, self).__init__(ActivityType.TowerStage)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "宝塔活动"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_tower_event_info()
        if info is None:
            return self.next_half_hour()

        if info["阶段"] == 1 and info["选中宝塔"] == 0:
            self.accept_by_tower_id(info["宝塔"][self.m_dictConfig["tower"]])
        elif info["阶段"] == 2 and info["状态"] == 0:
            self.finish_tower()

        return self.next_half_hour()

    def get_tower_event_info(self):
        url = "/root/festaval!getTowerEventInfo.action"
        result = self.get_xml(url, "宝塔活动")
        if result and result.m_bSucceed:
            info = dict()
            info["阶段"] = int(result.m_objResult["stage"])
            info["选中宝塔"] = int(result.m_objResult.get("curtowerid", "0"))
            info["宝塔"] = result.m_objResult["towerbaoshi"]
            info["状态"] = int(result.m_objResult["curstate"])
            return info

    def accept_by_tower_id(self, tower):
        url = "/root/festaval!acceptByTowerId.action"
        data = {"towerId": tower["id"]}
        result = self.post_xml(url, data, "选择宝塔")
        if result and result.m_bSucceed:
            self.info("选择宝塔[{}]，要求：{}宝石，奖励：{}宝石 {}筑造石".format(tower["name"], GlobalFunc.get_short_readable(int(tower["baoshi"])), GlobalFunc.get_short_readable(int(tower["reward"])), tower["rewardbuildingstone"]))

    def finish_tower(self):
        url = "/root/festaval!finishTower.action"
        result = self.get_xml(url, "完成宝塔")
        if result and result.m_bSucceed:
            reward = Reward()
            reward.type = 5
            reward.lv = 1
            reward.num = int(result.m_objResult["baoshi"])
            reward.init()
            reward_info = RewardInfo()
            reward_info.m_listRewards.append(reward)
            self.add_reward(reward_info)
            self.info("完成宝塔，获得{}筑造石，{}".format(result.m_objResult["buildingstone"], reward_info))
