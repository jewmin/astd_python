# -*- coding: utf-8 -*-
# 服务接口


class IServer(object):
    def __init__(self):
        super(IServer, self).__init__()

    def init_completed(self):
        pass

    def start(self):
        pass

    def stop(self, is_user_operate):
        pass

    def notify_state(self, status):
        pass

    def refresh_player(self):
        pass

    def notify_single_task(self, task_name):
        pass

    def start_re_login_timer(self):
        pass
