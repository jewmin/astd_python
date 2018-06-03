# -*- coding: utf-8 -*-
# 活动任务基类
import abc
from logic.base_task import BaseTask
from logic.activity.activity_config import activity_config


class ActivityTask(BaseTask):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(ActivityTask, self).__init__()
        self.m_szName = "activity"
        self.m_szReadable = "活动"
        self.m_ActivityMgr = None
        self.m_dictConfig = dict()

    def init(self):
        self.m_ActivityMgr = self.m_objServiceFactory.get_activity_mgr()
        self.m_dictConfig = activity_config[self.m_szName]

    def enable(self):
        return self.m_dictConfig.get("enable", False)
