# -*- coding: utf-8 -*-
# 征收任务
from logic.base_task import BaseTask
from logic.config import config


class ImposeTask(BaseTask):
    def __init__(self):
        super(ImposeTask, self).__init__()
        self.m_szName = "impose"
        self.m_szReadable = "征收"

    def run(self):
        if config["impose"]["auto_impose"]:
            city_mgr = self.m_objServiceFactory.get_city_mgr()
            impose_num, force_impose_cost = city_mgr.per_impose()
            if self.m_objUser.m_bImposeCdFlag:
                return self.m_objUser.m_nImposeCd
            if impose_num > config["impose"]["reserve"]:
                city_mgr.impose(False)
                return self.immediate()
            elif force_impose_cost <= config["impose"]["force"] and force_impose_cost <= self.get_available_gold():
                city_mgr.impose(True, force_impose_cost)
                return self.immediate()
            elif config["impose"]["finish_task"]:
                if not self.is_finish_task(2) and force_impose_cost <= self.get_available_gold():
                    city_mgr.impose(True, force_impose_cost)
                    return self.immediate()
                elif not self.is_finish_task(1) and impose_num > 0:
                    city_mgr.impose(False)
                    return self.immediate()

        return self.next_half_hour()
