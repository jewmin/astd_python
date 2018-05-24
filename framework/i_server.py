# -*- coding: utf-8 -*-
# 服务接口
import abc


class IServer(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(IServer, self).__init__()

    @abc.abstractmethod
    def init_completed(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self, is_user_operate):
        pass

    @abc.abstractmethod
    def notify_state(self, status):
        pass

    @abc.abstractmethod
    def refresh_player(self):
        pass

    @abc.abstractmethod
    def notify_single_task(self, task_name):
        pass

    @abc.abstractmethod
    def start_re_login_timer(self):
        pass
