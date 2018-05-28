# -*- coding: utf-8 -*-
# 强化任务
from logic.base_task import BaseTask
from logic.config import config


class EquipTask(BaseTask):
    def __init__(self):
        super(EquipTask, self).__init__()
        self.m_szName = "equip"
        self.m_szReadable = "强化"

    def run(self):
        equip_mgr = self.m_objServiceFactory.get_equip_mgr()

        # composite equipname generalname canupgrade xuli maxxuli
        # molicost canmoli attfull deffull powerstr.split(";")
        # tickets ticketsstatus
        monkey_config = config["equip"]["monkey"]
        if monkey_config["enable"]:
            dict_info = equip_mgr.get_upgrade_info()
            if dict_info is not None:
                upgrade = False
                for equipdto in dict_info["套装"]:
                    if int(equipdto["xuli"]) >= int(equipdto["maxxuli"]):
                        equip_mgr.use_xuli(equipdto)

                    if int(equipdto["tickets"]) <= monkey_config["use_tickets"] and equip_mgr.m_nTicketNumber > monkey_config["reverse_tickets"]:
                        equip_mgr.upgrade_monkey_tao(equipdto, 40)
                        upgrade = True

                if upgrade:
                    return self.immediate()

        goods_config = config["equip"]["goods"]
        if goods_config["enable"]:
            dict_info = equip_mgr.open_store_house()
            if dict_info is not None:
                for storehousedto in dict_info["物品"]:
                    if dict_info["使用"] < dict_info["总量"]:
                        if int(storehousedto["remaintime"]) > 0:
                            equip_mgr.draw(storehousedto)
                            dict_info["使用"] += 1
                    else:
                        break

        # baoshilevel composite equipstoreid hole istop storeid generalname goodsname
        crystal_config = config["equip"]["crystal"]
        if crystal_config["enable"]:
            dict_info = equip_mgr.get_crystal()
            if dict_info is not None:
                upgrade = False
                for baoshidto in dict_info["水晶石"]:
                    if baoshidto.get("istop", "0") == "1":
                        continue
                    if int(baoshidto["baoshilevel"]) >= crystal_config["level"]:
                        if not equip_mgr.upgrade_crystal(baoshidto):
                            return self.next_half_hour()
                        else:
                            upgrade = True

                if upgrade:
                    return self.immediate()

        return self.next_half_hour()
