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
        # composite equipname generalname canupgrade xuli maxxuli
        # molicost canmoli attfull deffull powerstr.split(";")
        # tickets ticketsstatus
        monkey_config = config["equip"]["monkey"]
        if monkey_config["enable"]:
            equip_mgr = self.m_objServiceFactory.get_equip_mgr()
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

        return self.next_half_hour()
