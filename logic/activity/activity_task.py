# -*- coding: utf-8 -*-
# 活动任务基类
import abc
from logic.base_task import BaseTask
from logic.activity.activity_config import activity_config


class ActivityTask(BaseTask):
    __metaclass__ = abc.ABCMeta

    def __init__(self, activity_type):
        super(ActivityTask, self).__init__()
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "活动"
        self.m_ActivityMgr = None
        self.m_dictConfig = dict()
        self.m_eActivityType = activity_type
        self.m_nConsumeGold = 0
        self.m_listRewardInfo = list()

    def init(self):
        self.m_ActivityMgr = self.m_objServiceFactory.get_activity_mgr()
        self.m_dictConfig = activity_config[self.m_szName]

    def enable(self):
        return self.m_dictConfig.get("enable", False) and self.has_activity()

    def has_activity(self):
        return self.m_objUser.m_dictActivities.get(self.m_eActivityType, False)

    def info(self, msg, use_gold=False):
        self.m_ActivityMgr.info(msg, use_gold)

    def get_xml(self, url, desc):
        return self.m_objProtocolMgr.get_xml(url, desc)

    def post_xml(self, url, data, desc):
        return self.m_objProtocolMgr.post_xml(url, data, desc)

    def consume_gold(self, gold):
        self.m_nConsumeGold += gold

    def add_reward(self, reward_info):
        for reward in reward_info.m_listRewards:
            has = False
            for my_reward in self.m_listRewardInfo:
                if my_reward == reward:
                    has = True
                    my_reward.num += reward.num
                    break
            if not has:
                self.m_listRewardInfo.append(reward)

    def has_reward(self):
        return self.m_nConsumeGold > 0 or len(self.m_listRewardInfo) > 0

    def __str__(self):
        reward_msg = ""
        first = True
        for item in self.m_listRewardInfo:
            if first:
                first = False
                reward_msg += "{}".format(item)
            else:
                reward_msg += " {}".format(item)
        return "活动[{}]：花费{}金币，获得{}".format(self.m_szReadable, self.m_nConsumeGold, reward_msg)
