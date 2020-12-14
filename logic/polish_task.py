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
        if dict_info is None:
            return self.next_half_hour()

        dict_info["装备的专属玉佩"] = list()
        dict_info["0属性的专属玉佩"] = list()
        for i in range(len(dict_info["专属玉佩"]) - 1, -1, -1):
            specialtreasure = dict_info["专属玉佩"][i]
            attribute_lea = int(specialtreasure["attribute_lea"])
            attribute_str = int(specialtreasure["attribute_str"])
            attribute_int = int(specialtreasure["attribute_int"])
            if attribute_lea == attribute_str == attribute_int == 0:
                dict_info["0属性的专属玉佩"].append(specialtreasure)
                dict_info["专属玉佩"].remove(specialtreasure)
            elif specialtreasure.get("generalname", None) is not None:
                dict_info["装备的专属玉佩"].append(specialtreasure)
                dict_info["专属玉佩"].remove(specialtreasure)
            elif attribute_lea >= 10 and attribute_str >= 10 and attribute_int >= 10 and "additionalattribute" in specialtreasure:
                additionalattribute = specialtreasure["additionalattribute"]["attribute"]
                if isinstance(additionalattribute, list) and len(additionalattribute) >= 3:
                    attribute_msg = ""
                    for attribute in additionalattribute:
                        attribute_msg += attribute + ", "
                    equip_mgr.warning("3属性超过10且有3个技能以上的专属玉佩[{}]({})".format(specialtreasure["storeid"], attribute_msg[:-2]))

        baowu_config = config["equip"]["polish"]["baowu"]
        dict_info["装备的家传玉佩"] = list()
        dict_info["日月光华"] = list()
        for i in range(len(dict_info["家传玉佩"]) - 1, -1, -1):
            baowu = dict_info["家传玉佩"][i]
            if baowu.get("generalname", None) is not None:
                dict_info["家传玉佩"].remove(baowu)
                attribute_lea = int(baowu["attribute_lea"]) + int(baowu["leaadd"])
                attribute_str = int(baowu["attribute_str"]) + int(baowu["stradd"])
                attribute_int = int(baowu["attribute_int"]) + int(baowu["intadd"])
                attribute_max = attribute_lea + attribute_str + attribute_int
                maxadd = int(baowu["maxadd"])
                if attribute_lea < maxadd or attribute_str < maxadd or attribute_int < maxadd:
                    if baowu["quality"] == "6":  # 紫宝
                        baowu["成功率"] = int(float(baowu["succprob"]) * 1000)
                    else:
                        baowu["成功率"] = int(float(baowu["succprob"]) * 10000)
                    if baowu["quality"] in baowu_config["quality"] and attribute_max < baowu_config["limit"]:
                        dict_info["装备的家传玉佩"].append(baowu)
            elif baowu["name"] == "日月光华" and baowu["attribute_lea"] == baowu["attribute_str"] == baowu["attribute_int"] == "50":
                dict_info["日月光华"].append(baowu)
                dict_info["家传玉佩"].remove(baowu)

        reverse_50 = config["equip"]["polish"]["reverse_50"]
        specialtreasure_config = config["equip"]["polish"]["specialtreasure"]
        if specialtreasure_config["enable"]:
            while len(dict_info["0属性的专属玉佩"]) > specialtreasure_config["reverse"]:
                equip_mgr.melt(dict_info["0属性的专属玉佩"].pop(), True)

            for specialtreasure in dict_info["装备的专属玉佩"]:
                if specialtreasure["generalname"] not in specialtreasure_config["include_general"]:
                    continue
                if not self.upgrade_specialtreasure(reverse_50, specialtreasure, dict_info["日月光华"], specialtreasure_config["attribute"], specialtreasure_config["include"], specialtreasure_config["available_attribute_len"]):
                    break

            for specialtreasure in dict_info["专属玉佩"]:
                if not self.upgrade_specialtreasure(reverse_50, specialtreasure, dict_info["日月光华"], specialtreasure_config["attribute"], specialtreasure_config["include"], specialtreasure_config["available_attribute_len"]):
                    break

        if baowu_config["enable"]:
            # dict_info["装备的家传玉佩"] = sorted(dict_info["装备的家传玉佩"], key=lambda value: int(value["maxadd"]), reverse=False)
            dict_info["装备的家传玉佩"] = sorted(dict_info["装备的家传玉佩"], key=lambda value: (value["成功率"], value["quality"]), reverse=True)
            for baowu in dict_info["装备的家传玉佩"]:
                if not self.upgrade_baowu(reverse_50, baowu, dict_info["日月光华"]):
                    break

        polish_config = config["equip"]["polish"]["polish"]
        if polish_config["enable"]:
            for baowu in dict_info["家传玉佩"]:
                success, dict_info["炼化机会"] = self.polish(baowu, dict_info["炼化机会"], polish_config["need_attrs"], polish_config["use_gold"])
                if not success:
                    break

        return self.next_half_hour()

    def upgrade_specialtreasure(self, reverse_50, specialtreasure, list_baowu, attribute_config, include_config, available_attribute_len_config):
        equip_mgr = self.m_objServiceFactory.get_equip_mgr()

        attribute_max = 35
        attribute_lea = int(specialtreasure["attribute_lea"])
        attribute_str = int(specialtreasure["attribute_str"])
        attribute_int = int(specialtreasure["attribute_int"])
        max_attribute = attribute_lea == attribute_max and attribute_str == attribute_max and attribute_int == attribute_max
        if "additionalattribute" in specialtreasure:
            if isinstance(specialtreasure["additionalattribute"]["attribute"], list):
                specialtreasure_attribute = specialtreasure["additionalattribute"]["attribute"]
            else:
                specialtreasure_attribute = [specialtreasure["additionalattribute"]["attribute"]]
            max_additionalattribute = True
            total_additionalattribute_len = len(specialtreasure_attribute)
            available_additionalattribute_len = 0
            for attribute in specialtreasure_attribute:
                attrs = attribute.split(":")
                if attrs[1] in attribute_config:
                    available_additionalattribute_len += 1
                    if attrs[2] != "3":
                        max_additionalattribute = False
            if max_attribute and max_additionalattribute:  # 跳过满属性和满技能
                return True
            if int(specialtreasure["storeid"]) not in include_config:
                if available_additionalattribute_len < available_attribute_len_config[total_additionalattribute_len]:
                    return True

        while len(list_baowu) > reverse_50:
            if specialtreasure.get("canconsecrate", "0") == "1":
                equip_mgr.consecrate_special_treasure(specialtreasure)
                return True

            if specialtreasure.get("canevolve", "0") == "1":
                equip_mgr.evolve_special_treasure(specialtreasure)
                return True

            upgrade_baowu = list_baowu.pop()
            if upgrade_baowu is not None:
                if not equip_mgr.upgrade_baowu(specialtreasure, upgrade_baowu, True):
                    return True

        return False

    def upgrade_baowu(self, reverse_50, baowu, list_baowu):
        equip_mgr = self.m_objServiceFactory.get_equip_mgr()
        while len(list_baowu) > reverse_50:
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
