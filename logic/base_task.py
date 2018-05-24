# -*- coding: utf-8 -*-
# 任务基类
from datetime import datetime
import pytz
from model.global_func import GlobalFunc
import abc


class BaseTask(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(BaseTask, self).__init__()
        self.m_objProtocolMgr = None
        self.m_objServiceFactory = None
        self.m_objUser = None
        self.m_objIServer = None
        self.m_szName = ""  # 唯一名称
        self.m_szReadable = ""  # 显示名称
        self.m_nNextRunningTimestamp = 0  # 下一次执行时间

    def __lt__(self, other):
        return self.get_next_running_time() < other.get_next_running_time()

    def __str__(self):
        dt = datetime.fromtimestamp(self.m_nNextRunningTimestamp / 1000, pytz.timezone("UTC"))
        return "{} : {}\r\n".format(dt.strftime("%H:%M:%S"), self.m_szReadable)

    def set_next_running_time(self, timestamp):
        self.m_nNextRunningTimestamp = self.m_objServiceFactory.get_time_mgr().get_timestamp() + timestamp

    def get_next_running_time(self):
        return self.m_nNextRunningTimestamp

    def set_variables(self, service_factory, protocol_mgr, user, i_server):
        self.m_objServiceFactory = service_factory
        self.m_objProtocolMgr = protocol_mgr
        self.m_objUser = user
        self.m_objIServer = i_server

    def init(self):
        pass

    @abc.abstractmethod
    def run(self):
        return 0

    def notify_single_task(self, task_name):
        if self.m_objIServer is not None:
            self.m_objIServer.notify_single_task(task_name)

    def get_available_gold(self):
        return GlobalFunc.get_available("gold", self.m_objUser.m_nGold + self.m_objUser.m_nRechargeGold)

    def get_available_copper(self):
        return GlobalFunc.get_available("copper", self.m_objUser.m_nCopper)

    def is_finish_task(self, task_type):
        task = self.m_objUser.m_dictTasks.get(task_type, None)
        if task is None or task.finishnum >= task.finishline:
            return True
        else:
            return False

    @staticmethod
    def immediate():
        return 2000

    @staticmethod
    def one_minute():
        return 60000

    @staticmethod
    def two_minute():
        return 120000

    @staticmethod
    def an_hour_later():
        return 3600000

    def next_half_hour(self):
        """距离下一半点相差的毫秒数"""
        minute = self.m_objServiceFactory.get_time_mgr().get_datetime().minute
        if minute < 30:
            remainder = 30 - minute
        else:
            remainder = 60 - minute
        return remainder * 60000

    def next_hour(self):
        """距离下一整点相差的毫秒数"""
        return (60 - self.m_objServiceFactory.get_time_mgr().get_datetime().minute) * 60000

    def next_day(self, next_hour=5):
        """距离第二天相差的毫秒数"""
        date_time = self.m_objServiceFactory.get_time_mgr().get_datetime()
        if date_time.hour < next_hour:
            remainder = next_hour - date_time.hour - 1
        else:
            remainder = 24 + next_hour - date_time.hour - 1
        return (remainder * 60 + 90 - date_time.minute) * 60000

    def next_dinner(self):
        """距离下一次宴会相差的毫秒数"""
        date_time = self.m_objServiceFactory.get_time_mgr().get_datetime()
        if date_time.hour < 10:
            remainder = 10 - date_time.hour - 1
        elif date_time.hour < 19:
            remainder = 19 - date_time.hour - 1
        else:
            remainder = 34 - date_time.hour - 1
        return (remainder * 60 + 90 - date_time.minute) * 60000
