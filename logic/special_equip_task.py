# -*- coding: utf-8 -*-
# 装备铸造任务
from logic.base_task import BaseTask
from logic.config import config


class SpecialEquipTask(BaseTask):
    def __init__(self):
        super(SpecialEquipTask, self).__init__()
        self.m_szName = "special_equip"
        self.m_szReadable = "装备铸造"

    def run(self):
        special_equip_config = config["equip"]["special_equip"]
        if special_equip_config["enable"]:
            equip_mgr = self.m_objServiceFactory.get_equip_mgr()
            dict_info = equip_mgr.get_special_equip_cast_info()
            if dict_info is not None:
                if dict_info["当前进度"] >= dict_info["总进度"]:
                    equip_mgr.special_equip_cast(2, "免费精火铸造")
                    return self.immediate()
                elif dict_info["免费铸造次数"] > 0:
                    equip_mgr.special_equip_cast(1, "免费铸造")
                    return self.immediate()
                elif dict_info["铸造消耗金币"] <= special_equip_config["firstcost"] and dict_info["铸造消耗金币"] <= self.get_available_gold():
                    equip_mgr.special_equip_cast(1, "花费{}金币铸造".format(dict_info["铸造消耗金币"]))
                    return self.immediate()
                elif dict_info["精火铸造消耗金币"] <= special_equip_config["secondcost"] and dict_info["精火铸造消耗金币"] <= self.get_available_gold():
                    equip_mgr.special_equip_cast(2, "花费{}金币精火铸造".format(dict_info["精火铸造消耗金币"]))
                    return self.immediate()

            dict_info = equip_mgr.get_all_special_equip()
            if dict_info is not None:
                for equipdto in dict_info["专属"]:
                    if int(equipdto["quality"]) <= special_equip_config["smelt"]["quality"]:
                        equip_mgr.smelt_special_equip(equipdto)
                    elif int(equipdto["equiplevel"]) <= special_equip_config["smelt"]["level"]:
                        equip_mgr.smelt_special_equip(equipdto)

        return self.next_half_hour()
