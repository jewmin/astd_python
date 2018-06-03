# -*- coding: utf-8 -*-
# 征战任务
from logic.base_task import BaseTask
from logic.config import config


class BattleTask(BaseTask):
    def __init__(self):
        super(BattleTask, self).__init__()
        self.m_szName = "battle"
        self.m_szReadable = "征战"

    def run(self):
        if config["battle"]["enable"]:
            battle_mgr = self.m_objServiceFactory.get_battle_mgr()
            info = battle_mgr.battle()
            if info["免费强攻令"] > 0 and config["battle"].get("armyid", 0) > 0:
                while info["免费强攻令"] > 0:
                    battle_mgr.battle_army(config["battle"]["armyid"], True)
                    info["免费强攻令"] -= 1
                return self.immediate()

            state = info["征战事件"].get("state", "0")
            if state == "1":
                process = map(int, info["征战事件"]["process"].split("/"))
                while process[0] < process[1]:
                    battle_mgr.do_battle_event()
                    process[0] += 1
                return self.immediate()
            elif state == "2":
                battle_mgr.recv_battle_event_reward()
                return self.immediate()

        return self.next_half_hour()
