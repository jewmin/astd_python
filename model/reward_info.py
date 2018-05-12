# -*- coding: utf-8 -*-
# 奖励
from model.base_object import BaseObject


class RewardInfo(object):
    def __init__(self):
        super(RewardInfo, self).__init__()
        self.m_listRewards = []

    def __str__(self):
        string = ""
        for item in self.m_listRewards:
            string += "{} ".format(str(item))
        return string

    def handle_info(self, list_info):
        if list_info is not None:
            for v in list_info:
                reward = Reward()
                reward.handle_info(v)
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
        return "{}(lv.{})+{}".format(self.itemname, self.lv, self.num)
