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

    def init(self):
        self.m_ActivityMgr = self.m_objServiceFactory.get_activity_mgr()
        self.m_dictConfig = activity_config[self.m_szName]

    def enable(self):
        return self.m_dictConfig.get("enable", False) and self.has_activity()

    def has_activity(self):
        return self.m_objUser.m_dictActivities.get(self.m_eActivityType, False)

    def info(self, msg, use_gold=False):
        self.m_ActivityMgr.info(msg, use_gold)
