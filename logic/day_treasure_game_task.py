# -*- coding: utf-8 -*-
# 王朝寻宝任务
from logic.base_task import BaseTask
from logic.config import config


class DayTreasureGameTask(BaseTask):
    def __init__(self):
        super(DayTreasureGameTask, self).__init__()
        self.m_szName = "day_treasure_game"
        self.m_szReadable = "王朝寻宝"

    def run(self):
        if config["dayTreasureGame"]["enable"]:
            misc_mgr = self.m_objServiceFactory.get_misc_mgr()
            dict_info = misc_mgr.start_new_t_game()
            if dict_info is not None:
                if "事件" in dict_info:
                    self.handle_event(dict_info)
                    return self.immediate()

                if dict_info["换地图"]:
                    misc_mgr.transfer()
                    return self.immediate()

                if dict_info["探宝完毕"]:
                    misc_mgr.away_new_t_game()
                    return self.immediate()

                if float(self.m_objUser.m_nCurActive) / float(self.m_objUser.m_nMaxActive) <= config["dayTreasureGame"]["active_proportion"]:
                    if dict_info["当前骰子"] > 0:
                        misc_mgr.use_new_t_dice()
                        return self.immediate()

        return self.next_half_hour()

    def handle_event(self, dict_info):
        misc_mgr = self.m_objServiceFactory.get_misc_mgr()
        if dict_info["事件"] == "1":
            misc_mgr.handler_event(1, "执行[探索路径]事件，行走第{}步".format(dict_info["探索路径步数"]))
        elif dict_info["事件"] == "2":
            if dict_info["免费摇摇钱树"] > 0:
                misc_mgr.handler_event(1, "执行[摇钱树]事件，免费摇")
            else:
                misc_mgr.handler_event(0, "取消[摇钱树]事件，下一次宝石奖励[{}]".format(dict_info["下一次宝石奖励"]))
        elif dict_info["事件"] == "3":
            misc_mgr.handler_event(0, "取消[购买]事件，宝箱[{}({}金币)]".format(dict_info["购买宝箱"], dict_info["购买宝箱消耗金币"]))
