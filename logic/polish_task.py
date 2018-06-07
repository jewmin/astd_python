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
        dict_info = equip_mgr.get_bao_wu_polish_info()

        dict_info["装备的专属玉佩"] = list()
        dict_info["0属性的专属玉佩"] = list()
        for i in range(len(dict_info["专属玉佩"]) - 1, -1, -1):
            specialtreasure = dict_info["专属玉佩"][i]
            if specialtreasure["attribute_lea"] == specialtreasure["attribute_str"] == specialtreasure["attribute_int"] == "0":
                dict_info["0属性的专属玉佩"].append(specialtreasure)
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
            while len(dict_info["0属性的专属玉佩"]) > specialtreasure_config["reverse"]:
                equip_mgr.melt(dict_info["0属性的专属玉佩"].pop(), True)

            for specialtreasure in dict_info["装备的专属玉佩"]:
                if not self.upgrade_specialtreasure(specialtreasure, dict_info["日月光华"], specialtreasure_config["attribute"]):
                    break

            for specialtreasure in dict_info["专属玉佩"]:
                if not self.upgrade_specialtreasure(specialtreasure, dict_info["日月光华"], specialtreasure_config["attribute"]):
                    break

        baowu_config = config["equip"]["polish"]["baowu"]
        if baowu_config["enable"]:
            dict_info["装备的家传玉佩"] = sorted(dict_info["装备的家传玉佩"], key=lambda value: int(value["maxadd"]), reverse=True)
            for baowu in dict_info["装备的家传玉佩"]:
                if not self.upgrade_baowu(baowu, dict_info["日月光华"]):
                    break

        polish_config = config["equip"]["polish"]["polish"]
        if polish_config["enable"]:
            for baowu in dict_info["家传玉佩"]:
                success, dict_info["炼化机会"] = self.polish(baowu, dict_info["炼化机会"], polish_config["need_attrs"], polish_config["use_gold"])
                if not success:
                    break

        return self.next_half_hour()

    def upgrade_specialtreasure(self, specialtreasure, list_baowu, attribute_config):
        equip_mgr = self.m_objServiceFactory.get_equip_mgr()
        while len(list_baowu) > 0:
            if specialtreasure.get("canconsecrate", "0") == "1":
                equip_mgr.consecrate_special_treasure(specialtreasure)
                return True

            if specialtreasure.get("canevolve", "0") == "1":
                equip_mgr.evolve_special_treasure(specialtreasure)
                return True

            if "additionalattribute" in specialtreasure:
                if isinstance(specialtreasure["additionalattribute"]["attribute"], list):
                    for attribute in specialtreasure["additionalattribute"]["attribute"]:
                        attrs = attribute.split(":")
                        if attrs[1] not in attribute_config:
                            return True
                else:
                    attrs = specialtreasure["additionalattribute"]["attribute"].split(":")
                    if attrs[1] not in attribute_config:
                        return True

            upgrade_baowu = list_baowu.pop()
            if upgrade_baowu is not None:
                if not equip_mgr.upgrade_baowu(specialtreasure, upgrade_baowu, True):
                    return True

        return False

    def upgrade_baowu(self, baowu, list_baowu):
        equip_mgr = self.m_objServiceFactory.get_equip_mgr()
        while len(list_baowu) > 0:
            upgrade_baowu = list_baowu.pop()
            if upgrade_baowu is not None:
                if not equip_mgr.upgrade_baowu(baowu, upgrade_baowu):
                    return True

        return False

    def polish(self, baowu, num, need_attrs, use_gold):
        equip_mgr = self.m_objServiceFactory.get_equip_mgr()
        while num > 0:
            polishtimes = baowu["polishtimes"]
            attribute_base = int(baowu["attribute_base"])
            gold = int(baowu["gold"])
            if attribute_base < need_attrs[polishtimes]:
                equip_mgr.melt(baowu)
                return True, num
            elif gold == 0:
                num -= 1
                if not equip_mgr.polish(baowu):
                    return True, num
            elif use_gold and gold <= self.get_available_gold():
                num -= 1
                if not equip_mgr.polish(baowu, True):
                    return True, num
            else:
                return True, num

        return False, num
