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
        polish_config = config["equip"]["polish"]["polish"]
        dict_info = equip_mgr.get_bao_wu_polish_info()

        dict_info["装备的专属玉佩"] = list()
        for i in range(len(dict_info["专属玉佩"]) - 1, -1, -1):
            specialtreasure = dict_info["专属玉佩"][i]
            if specialtreasure["attribute_lea"] == specialtreasure["attribute_str"] == specialtreasure["attribute_int"] == "0":
                dict_info["专属玉佩"].remove(specialtreasure)
            elif specialtreasure.get("generalname", None) is not None:
                dict_info["装备的专属玉佩"].append(specialtreasure)
                dict_info["专属玉佩"].remove(specialtreasure)

        dict_info["装备的家传玉佩"] = list()
        dict_info["日月光华"] = list()
        for i in range(len(dict_info["家传玉佩"]) - 1, -1, -1):
            baowu = dict_info["家传玉佩"][i]
            if baowu.get("generalname", None) is not None:
                dict_info["装备的家传玉佩"].append(baowu)
                dict_info["家传玉佩"].remove(baowu)
            elif baowu["name"] == "日月光华" and baowu["attribute_lea"] == baowu["attribute_str"] == baowu["attribute_int"] == "50":
                dict_info["日月光华"].append(baowu)
                dict_info["家传玉佩"].remove(baowu)

        if polish_config["enable"]:
            min_attr_polishtimes = polish_config["min_attr"][0]
            min_attr_attribute_base = polish_config["min_attr"][1]
            attr_polishtimes = polish_config["times_and_attrs"][0]
            attr_attribute_base = polish_config["times_and_attrs"][1]
            for i in range(len(dict_info["家传玉佩"]) - 1, -1, -1):
                baowu = dict_info["家传玉佩"][i]
                polishtimes = int(baowu["polishtimes"])
                attribute_base = int(baowu["attribute_base"])
                if polishtimes == min_attr_polishtimes and attribute_base < min_attr_attribute_base:
                    equip_mgr.melt(baowu)
                    dict_info["家传玉佩"].remove(baowu)
                elif polishtimes == attr_polishtimes and attribute_base < attr_attribute_base:
                    equip_mgr.melt(baowu)
                    dict_info["家传玉佩"].remove(baowu)

            if dict_info["炼化机会"] >= polish_config["min_num"]:
                pass

        return self.next_half_hour()
