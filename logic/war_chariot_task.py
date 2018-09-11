# -*- coding: utf-8 -*-
# 战车强化任务
from logic.base_task import BaseTask
from logic.config import config


class WarChariotTask(BaseTask):
    def __init__(self):
        super(WarChariotTask, self).__init__()
        self.m_szName = "war_chariot"
        self.m_szReadable = "战车强化"

    def run(self):
        war_chariot_config = config["equip"]["war_chariot"]
        war_drum_config = config["equip"]["war_drum"]
        if war_chariot_config["enable"]:
            equip_mgr = self.m_objServiceFactory.get_equip_mgr()
            misc_mgr = self.m_objServiceFactory.get_misc_mgr()
            active_mgr = self.m_objServiceFactory.get_active_mgr()
            dict_info = equip_mgr.get_war_chariot_info()
            if dict_info is not None:
                if dict_info["当前等级"] >= 100:
                    if war_drum_config["enable"]:
                        refine_info = active_mgr.get_refine_info()
                        war_drum_info = equip_mgr.get_war_drum_info()
                        if refine_info is not None and war_drum_info is not None:
                            if refine_info["当前余料"] < int(refine_info["余料上限"] * war_drum_config["refine_rate"]):
                                for v in war_drum_config["sort"]:
                                    war_drum = war_drum_info["战鼓列表"][v]
                                    if self.can_upgrade_war_drum(war_drum, war_drum_info):
                                        equip_mgr.strengthen_war_drum(v)
                                        return self.immediate()
                    return self.next_half_hour()

                if dict_info["消耗兵器"] > war_chariot_config["equipment_num"]:
                    return self.next_day()

                if dict_info["消耗兵器"] > dict_info["库存兵器"]:
                    if war_chariot_config["auto_exchange_weapon"]:
                        misc_mgr.get_tickets_reward_by_name("无敌将军炮", 10000)
                        return self.immediate()
                    else:
                        return self.next_half_hour()

                if dict_info["消耗玉石"] > dict_info["库存玉石"]:
                    if war_chariot_config["auto_exchange_bowlder"]:
                        misc_mgr.get_tickets_reward_by_name("玉石", 10)
                        return self.immediate()
                    else:
                        return self.next_half_hour()

                if war_chariot_config["only_use_hammer"]:
                    for hammer in dict_info["铁锤列表"]:
                        num = int(hammer["num"])
                        cri = int(hammer["cri"])
                        if num > 0 and cri <= war_chariot_config["hammer_level"]:
                            success = equip_mgr.strengthen_war_chariot(cri, "花费{}兵器碎片、{}玉石".format(dict_info["消耗兵器"], dict_info["消耗玉石"]))
                            if success:
                                return self.immediate()
                            else:
                                return self.next_half_hour()
                else:
                    cri = 0
                    for hammer in dict_info["铁锤列表"]:
                        num = int(hammer["num"])
                        if num > 0:
                            cri = int(hammer["cri"])
                            break
                    success = equip_mgr.strengthen_war_chariot(cri, "花费{}兵器碎片、{}玉石".format(dict_info["消耗兵器"], dict_info["消耗玉石"]))
                    if success:
                        return self.immediate()
                    else:
                        return self.next_half_hour()

        return self.next_half_hour()

    @staticmethod
    def can_upgrade_war_drum(war_drum, war_drum_info):
        return war_drum["当前等级"] < war_drum_info["最大等级"] and war_drum["消耗镔铁"] <= war_drum_info["库存镔铁"] and war_drum["消耗玉石"] <= war_drum_info["库存玉石"] and war_drum["消耗点券"] <= war_drum_info["库存点券"]
