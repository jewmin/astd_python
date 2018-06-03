# -*- coding: utf-8 -*-
# 宴会任务
from logic.base_task import BaseTask
from logic.config import config


class DinnerTask(BaseTask):
    def __init__(self):
        super(DinnerTask, self).__init__()
        self.m_szName = "dinner"
        self.m_szReadable = "宴会"

    def run(self):
        if config["dinner"]["enable"]:
            misc_mgr = self.m_objServiceFactory.get_misc_mgr()
            info = misc_mgr.get_all_dinner()
            if info is not None:
                if info["宴会期间"] and info["剩余宴会次数"] > 0:
                    if not info["已加入队伍"] and info.get("宴会队伍", None) is not None:
                        misc_mgr.join_dinner(info["宴会队伍"])
                    return self.immediate()

        return self.next_half_hour()
