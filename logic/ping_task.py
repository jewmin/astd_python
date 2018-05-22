# -*- coding: utf-8 -*-
# 会话保持任务
from logic.base_task import BaseTask


class PingTask(BaseTask):
    def __init__(self):
        super(PingTask, self).__init__()
        self.m_szName = "ping"
        self.m_szReadable = "会话保持"

    def run(self):
        misc_mgr = self.m_objServiceFactory.get_misc_mgr()
        misc_mgr.get_server_time()
        misc_mgr.get_player_extra_info2()
        return self.two_minute()
