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
        for item in self.m_listRewards:
            string += "{} ".format(item)
        return string

    def handle_info(self, list_info):
        if list_info is not None:
            if isinstance(list_info, list):
                for v in list_info:
                    reward = Reward()
                    reward.handle_info(v)
                    self.m_listRewards.append(reward)
            else:
                reward = Reward()
                reward.handle_info(list_info)
                self.m_listRewards.append(reward)


class Reward(BaseObject):
    def __init__(self):
        super(Reward, self).__init__()
        self.type = 0
        self.itemname = ""
        self.quality = 0
        self.lv = 0
        self.num = 0

    def __str__(self):
        if self.itemname == "" and self.type < len(config["reward"]["name"]):
            self.itemname = config["reward"]["name"][self.type]
        return "{}(lv.{})+{}".format(self.itemname, self.lv, GlobalFunc.get_short_readable(self.num))
