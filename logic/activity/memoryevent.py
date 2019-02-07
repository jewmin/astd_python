# -*- coding: utf-8 -*-
# 新春拜年
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo, Reward


class MemoryEvent(ActivityTask):
    def __init__(self):
        super(MemoryEvent, self).__init__(ActivityType.MemoryEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "新春拜年"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_memory_event_info()
        if info is None:
            return self.next_half_hour()

        if info["红包"] is not None:
            for hongbao in info["红包"]:
                if hongbao["canopen"] == "1":
                    if int(hongbao["num"]) > 0:
                        self.open_hongbao(hongbao["id"])
                        return self.immediate()
                    elif int(hongbao["cost"]) <= self.m_dictConfig["hongbaocost"]:
                        self.open_hongbao(hongbao["id"], int(hongbao["cost"]))
                        return self.immediate()

        if info["回忆图"] is not None:
            for picreward in info["回忆图"]:
                if picreward["state"] == "1":
                    self.open_pic_reward(picreward["id"])
                    return self.immediate()

        if info["拜年免费次数"] > 0:
            self.new_year_visit()
            return self.immediate()
        elif info["拜年花费金币"] <= self.m_dictConfig["wishcost"]:
            self.new_year_visit(info["拜年花费金币"])
            return self.immediate()

        return self.next_half_hour()

    def get_memory_event_info(self):
        url = "/root/memoryEvent!getMemoryEventInfo.action"
        result = self.get_xml(url, "新春拜年")
        if result and result.m_bSucceed:
            info = dict()
            info["拜年免费次数"] = int(result.m_objResult.get("freetimes", "0"))
            info["拜年花费金币"] = int(result.m_objResult.get("wishcost", "100"))
            info["红包"] = result.m_objResult.get("hongbao", None)
            info["回忆图"] = result.m_objResult.get("picreward", None)
            info["点亮武将"] = result.m_objResult.get("general", None)
            return info

    def new_year_visit(self, gold=0):
        url = "/root/memoryEvent!newYearVisit.action"
        result = self.get_xml(url, "拜年")
        if result and result.m_bSucceed:
            name = result.m_objResult["name"]
            light = int(result.m_objResult.get("light", "0"))
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.consume_gold(gold)
            if gold > 0:
                use_gold = True
                msg = "花费{}金币".format(gold)
            else:
                use_gold = False
                msg = "免费"
            self.info("{}新春拜年, 和武将[{}]拜年{}, 获得{}".format(msg, name, "点亮武将" if light > 0 else "", reward_info), use_gold)

    def open_pic_reward(self, id):
        url = "/root/memoryEvent!openPicReward.action"
        data = {"rewardId": id}
        result = self.post_xml(url, data, "回忆图")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("新春拜年, 领取回忆图奖励, 获得{}".format(reward_info))

    def open_hongbao(self, id, gold=0):
        url = "/root/memoryEvent!openHongbao.action"
        data = {"type": id}
        result = self.post_xml(url, data, "红包")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.consume_gold(gold)
            if gold > 0:
                use_gold = True
                msg = "花费{}金币".format(gold)
            else:
                use_gold = False
                msg = "免费"
            self.info("{}新春拜年, 领取红包, 获得{}".format(msg, reward_info), use_gold)
