# -*- coding: utf-8 -*-
# 奖励
from model.base_object import BaseObject
from logic.config import config
from model.global_func import GlobalFunc


class RewardInfo(object):
    def __init__(self):
        super(RewardInfo, self).__init__()
        self.m_listRewards = list()

    def __str__(self):
        string = ""
        first = True
        for item in self.m_listRewards:
            if first:
                first = False
                string += "{}".format(item)
            else:
                string += " {}".format(item)
        return string

    def get_reward(self, index):
        if index < len(self.m_listRewards):
            return self.m_listRewards[index]

    def handle_info(self, list_info):
        if list_info is not None:
            if isinstance(list_info, list):
                for v in list_info:
                    reward = Reward()
                    reward.handle_info(v["reward"])
                    reward.init()
                    self.m_listRewards.append(reward)
            elif isinstance(list_info["reward"], list):
                for v in list_info["reward"]:
                    reward = Reward()
                    reward.handle_info(v)
                    reward.init()
                    self.m_listRewards.append(reward)
            else:
                reward = Reward()
                reward.handle_info(list_info["reward"])
                reward.init()
                self.m_listRewards.append(reward)


class Reward(BaseObject):
    def __init__(self):
        super(Reward, self).__init__()
        self.type = 0
        self.itemname = ""
        self.quality = 0
        self.lv = 0
        self.num = 0

    def init(self):
        if self.itemname == "" and self.type < len(config["reward"]["name"]):
            self.itemname = config["reward"]["name"][self.type]

    def __str__(self):
        return "{}(lv.{})+{}".format(self.itemname, self.lv, GlobalFunc.get_short_readable(self.num))

    def __eq__(self, other):
        return self.type == other.type and self.itemname == other.itemname and self.lv == other.lv and self.quality == other.quality
