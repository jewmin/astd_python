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

        specialtreasure_config = config["equip"]["polish"]["specialtreasure"]
        if specialtreasure_config["enable"]:
            pass

        if polish_config["enable"]:
            need_attrs = polish_config["need_attrs"]
            for i in range(len(dict_info["家传玉佩"]) - 1, -1, -1):
                baowu = dict_info["家传玉佩"][i]
                polishtimes = baowu["polishtimes"]
                attribute_base = int(baowu["attribute_base"])
                gold = int(baowu["gold"])
                while True:
                    if attribute_base < need_attrs[polishtimes]:
                        equip_mgr.melt(baowu)
                        dict_info["家传玉佩"].remove(baowu)
                        break
                    elif dict_info["炼化机会"] <= 0:
                        break
                    elif gold == 0:
                        polishtimes, attribute_base, gold = equip_mgr.polish(baowu)
                        dict_info["炼化机会"] -= 1
                    elif polish_config["use_gold"] and gold <= self.get_available_gold():
                        olishtimes, attribute_base, gold = equip_mgr.polish(baowu)
                        dict_info["炼化机会"] -= 1
                    else:
                        break

        return self.next_half_hour()
