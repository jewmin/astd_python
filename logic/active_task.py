# -*- coding: utf-8 -*-
# 行动力任务
from logic.base_task import BaseTask
from logic.config import config


class ActiveTask(BaseTask):
    def __init__(self):
        super(ActiveTask, self).__init__()
        self.m_szName = "active"
        self.m_szReadable = "行动力"

    def run(self):
        if self.m_objUser.m_nCurActive > config["active"]["reserve"]:
            for v in config["active"]["sort"]:
                if not config["active"][v]["enable"]:
                    continue

                if v == "royalty":
                    pass
                elif v == "refine":
                    pass
                elif v == "refine_bin_tie":
                    pass
                elif v == "caravan":
                    pass

        return self.next_half_hour()
