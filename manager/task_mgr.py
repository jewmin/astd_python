# -*- coding: utf-8 -*-
# 任务管理
from logging import getLogger


class TaskMgr(object):
    def __init__(self):
        super(TaskMgr, self).__init__()
        self.logger = getLogger(self.__class__.__name__)
        self.m_objServiceFactory = None
        self.m_objUser = None
        self.m_listTasks = list()
        self.m_dictTasks = dict()
        self.m_szStatus = ""

    def find_task(self, task_name):
        return self.m_dictTasks.get(task_name, None)

    def add_task(self, task):
        if task is not None and task.m_szName != "":
            if self.find_task(task.m_szName) is None:
                self.m_listTasks.append(task)
                self.m_dictTasks[task.m_szName] = task

    def set_variables(self, service_factory, protocol_mgr, user):
        self.m_objServiceFactory = service_factory
        self.m_objUser = user
        for item in self.m_listTasks:
            item.set_variables(service_factory, protocol_mgr, self.m_objUser)

    def reset_running_time(self):
        for item in self.m_listTasks:
            item.set_next_running_time(0)

    def init(self):
        for item in self.m_listTasks:
            item.init()

    def run_all_task(self):
        timestamp = self.m_objServiceFactory.get_time_mgr().get_timestamp()
        for item in self.m_listTasks:
            if item.get_next_running_time() <= timestamp:
                try:
                    next_running_time = item.run()
                    item.set_next_running_time(next_running_time)
                except Exception as ex:
                    self.logger.error("执行任务[{}]报错：{}".format(item.m_szReadable, str(ex)))
                    item.set_next_running_time(item.next_half_hour())
        self.m_szStatus = ""
        self.m_listTasks.sort()
        for item in self.m_listTasks:
            self.m_szStatus += str(item)

    def run_single_task(self, task_name):
        task = self.find_task(task_name)
        if task is not None:
            next_running_time = task.run()
            task.set_next_running_time(next_running_time)
