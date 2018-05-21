# -*- coding: utf-8 -*-
# 点券商城任务
from logic.base_task import BaseTask
from logic.config import config


class TicketTask(BaseTask):
    def __init__(self):
        super(TicketTask, self).__init__()
        self.m_szName = "ticket"
        self.m_szReadable = "点券商城"

    def run(self):
        self.init()
        return self.next_half_hour()

    def init(self):
        if config["tickets"]["auto_exchange"]:
            misc_mgr = self.m_objServiceFactory.get_misc_mgr()
            ticket_list = misc_mgr.tickets()
            config_hero_list = config["tickets"]["hero"]["list"]
            config_hero_limit_tickets = config["tickets"]["hero"]["limit_tickets"]
            config_once_on_day_list = config["tickets"]["once_on_day"]["list"]
            config_more_on_day_list = config["tickets"]["more_on_day"]["list"]
            self.m_objUser.m_dictTicketExchange = dict()
            for v in ticket_list:
                if config["tickets"]["hero"]["enable"]:
                    if v.item.name in config_hero_list and v.tickets <= config_hero_limit_tickets:
                        misc_mgr.get_tickets_reward(v, 1)

                if config["tickets"]["once_on_day"]["enable"]:
                    sell_type = config_once_on_day_list.get(v.item.name, None)
                    if sell_type is not None and v.selltype == sell_type:
                        misc_mgr.get_tickets_reward(v, 1)

                if config["tickets"]["more_on_day"]["enable"]:
                    sell_type = config_more_on_day_list.get(v.item.name, None)
                    if sell_type is not None and v.selltype == sell_type:
                        self.m_objUser.m_dictTicketExchange[v.item.name] = v
