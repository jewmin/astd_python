# -*- coding: utf-8 -*-
# 炼化任务
from logic.base_task import BaseTask
from logic.config import config


class PolishTask(BaseTask):
    def __init__(self):
        super(PolishTask, self).__init__()
        self.m_szName = "polish"
        self.m_szReadable = "炼化"

    def run(self):
        equip_mgr = self.m_objServiceFactory.get_equip_mgr()
        polish_config = config["polish"]["polish"]
        if polish_config["enable"]:
            dict_info = equip_mgr.get_bao_wu_polish_info()
            if dict_info["炼化机会"] >= polish_config["min_num"]:
                min_attr_polishtimes = polish_config["min_attr"][0]
                min_attr_attribute_base = polish_config["min_attr"][1]
                attr_polishtimes = polish_config["times_and_attrs"][0]
                attr_attribute_base = polish_config["times_and_attrs"][1]
                for baowu in dict_info["家传玉佩"]:
                    polishtimes = int(baowu["polishtimes"])
                    attribute_base = int(baowu["attribute_base"])
                    if polishtimes == min_attr_polishtimes and attribute_base < min_attr_attribute_base:
                        equip_mgr.melt(baowu)
                    elif polishtimes == attr_polishtimes and attribute_base < attr_attribute_base:
                        equip_mgr.melt(baowu)

        return self.next_half_hour()
