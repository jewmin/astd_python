# -*- coding: utf-8 -*-
# 祭祀任务
from logic.base_task import BaseTask
from logic.config import config


class FeteTask(BaseTask):
    def __init__(self):
        super(FeteTask, self).__init__()
        self.m_szName = "fete"
        self.m_szReadable = "祭祀"

    def run(self):
        if config["fete"]["auto_fete"]:
            fete_gem_task = self.m_objUser.m_dictTasks.get(3, None)
            big_fete_task = self.m_objUser.m_dictTasks.get(4, None)
            if fete_gem_task is not None and fete_gem_task.finishline == 15:
                fete_config = config["fete"]["task15"]
            elif big_fete_task is not None and big_fete_task.finishline == 50:
                fete_config = config["fete"]["task50"]
            else:
                fete_config = config["fete"]["common"]
            misc_mgr = self.m_objServiceFactory.get_misc_mgr()
            fete_list, free_all_fete = misc_mgr.fete()
            for item in fete_list:
                if item.gold <= fete_config.get(item.name, 0) and item.gold <= self.get_available_gold():
                    misc_mgr.do_fete(item.id, item.gold, item.name)
                    return self.immediate()
            if free_all_fete > 0:
                misc_mgr.do_fete(6, 0, "大祭祀")
                return self.immediate()

        return self.next_half_hour()

    def init(self):
        pass
