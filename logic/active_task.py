# -*- coding: utf-8 -*-
# 行动力任务
from logic.base_task import BaseTask
from logic.config import config
from model.global_func import GlobalFunc


class ActiveTask(BaseTask):
    def __init__(self):
        super(ActiveTask, self).__init__()
        self.m_szName = "active"
        self.m_szReadable = "行动力"

    def run(self):
        if self.m_objUser.m_nCurActive > config["active"]["reserve"]:
            active_mgr = self.m_objServiceFactory.get_active_mgr()
            misc_mgr = self.m_objServiceFactory.get_misc_mgr()
            equip_mgr = self.m_objServiceFactory.get_equip_mgr()
            for v in config["active"]["sort"]:
                active_config = config["active"][v]
                if not active_config["enable"]:
                    continue

                if v == "royalty":
                    info = active_mgr.royalty_weave_info2()
                    if info is None:
                        return self.next_half_hour()

                    if info["消耗行动力"] > self.m_objUser.m_nCurActive:
                        return self.next_half_hour()

                    if info["布匹"] < info["布匹上限"]:
                        if active_config["do_high"] and info["剩余高效次数"] > 0:
                            active_mgr.royalty_weave2(info["消耗行动力"], 1)
                            return self.immediate()

                        if active_config["do_tired"] and info["剩余极限次数"] > 0:
                            active_mgr.royalty_weave2(info["消耗行动力"], 1)
                            return self.immediate()

                        if active_config["finish_task"] and not self.is_finish_task(12):
                            active_mgr.royalty_weave2(info["消耗行动力"], 1)
                            return self.immediate()

                    refresh_list = active_config["list"]
                    convert_cost = active_config["cost"]
                    if info["布匹"] >= active_config["limit"]["limit"]:
                        refresh_list = active_config["limit"]["list"]
                        convert_cost = active_config["limit"]["cost"]
                    has_trader = info["商人"] in refresh_list
                    if not has_trader and info["刷新商人费用"] <= active_config["refresh"]:
                        active_mgr.refresh_royalty_weave_new(info["刷新商人费用"])
                        return self.immediate()

                    if has_trader:
                        reward = info["换购商品"].get_reward(0)
                        if reward is not None:
                            for cost in convert_cost:
                                if cost["type"] == reward.type and cost["lv"] == reward.lv and cost["num"] == reward.num:
                                    if info["换购消耗布匹"] <= cost["needweavenum"] and info["换购消耗布匹"] <= info["布匹"]:
                                        active_mgr.convert_royalty_weave_new2(info["换购消耗布匹"])
                                    break

                elif v == "refine":
                    info = active_mgr.get_refine_info()
                    if info is None:
                        return self.next_half_hour()

                    if not info["可精炼工人"]:
                        return self.one_minute()

                    if info["消耗余料"] > info["当前余料"]:
                        # return self.next_half_hour()
                        continue

                    if info["消耗行动力"] > self.m_objUser.m_nCurActive:
                        return self.next_half_hour()

                    if info["消耗银币"] > self.get_available_copper():
                        misc_mgr.get_tickets_reward_by_name("银币", 10)

                    if info["升级单个工人消耗金币"] <= active_config["refresh_refiner"]["per_cost"]:
                        info["工人们"] = sorted(info["工人们"], key=lambda value: value["id"], reverse=True)
                        sn = ""
                        for var in info["工人们"]:
                            sn += var["id"]
                        if sn in active_config["refresh_refiner"]["list"]:
                            index = active_config["refresh_refiner"]["list"][sn]
                            active_mgr.refresh_one_refiner(info["工人们"][index], info["升级单个工人消耗金币"])
                        active_mgr.refine(info["消耗银币"], info["消耗行动力"])
                        return self.immediate()

                    if active_config["do_high"] and info["剩余高效次数"] > 0:
                        active_mgr.refine(info["消耗银币"], info["消耗行动力"])
                        return self.immediate()

                    if active_config["do_tired"] and info["剩余极限次数"] > 0:
                        active_mgr.refine(info["消耗银币"], info["消耗行动力"])
                        return self.immediate()

                    if active_config["finish_task"] and not self.is_finish_task(9):
                        active_mgr.refine(info["消耗银币"], info["消耗行动力"])
                        return self.immediate()

                elif v == "refine_bin_tie":
                    info = active_mgr.get_refine_bin_tie_factory()
                    if info is None:
                        return self.next_half_hour()

                    if info["消耗行动力"] > self.m_objUser.m_nCurActive:
                        return self.next_half_hour()

                    if info["消耗银币"] > self.get_available_copper():
                        misc_mgr.get_tickets_reward_by_name("银币", 10)

                    war_chariot_info = equip_mgr.get_war_chariot_info()
                    if war_chariot_info is None:
                        continue

                    mode = active_config["mode"]
                    if war_chariot_info["当前等级"] >= 100:
                        mode = 1

                    if active_config["do_high"] and info["剩余高效次数"] > 0:
                        active_mgr.do_refine_bin_tie_factory(info["消耗银币"], info["消耗行动力"], mode)
                        return self.immediate()

                    if active_config["do_tired"] and info["剩余极限次数"] > 0:
                        active_mgr.do_refine_bin_tie_factory(info["消耗银币"], info["消耗行动力"], mode)
                        return self.immediate()

                    if active_config["finish_task"] and not self.is_finish_task(10):
                        active_mgr.do_refine_bin_tie_factory(info["消耗银币"], info["消耗行动力"], mode)
                        return self.immediate()

                elif v == "caravan":
                    info = active_mgr.get_western_trade_info()
                    if info is None:
                        return self.next_half_hour()

                    if info["进入下一站"]:
                        active_mgr.next_place()

                    if "事件" in info:
                        self.handle_event(info)
                        return self.immediate()

                    info["商人们"] = sorted(info["商人们"], key=lambda value: value["active"])
                    for trader in info["商人们"]:
                        trader_active = int(trader["active"])
                        if trader_active > active_config["limit"]["active"] or trader_active > self.m_objUser.m_nCurActive:
                            continue
                        cost = trader["cost"].split(":")
                        real_cost = int(cost[1])
                        if cost[0] == "gold":
                            if real_cost <= active_config["limit"]["gold"] and real_cost <= self.get_available_gold():
                                info = active_mgr.western_trade(trader["id"], {"金币": real_cost, "行动力": trader_active})
                                self.handle_event(info)
                                return self.immediate()
                        elif cost[0] == "copper":
                            if real_cost <= active_config["limit"]["copper"]:
                                if real_cost > self.get_available_copper():
                                    misc_mgr.get_tickets_reward_by_name("银币", 10)
                                info = active_mgr.western_trade(trader, {"银币": GlobalFunc.get_short_readable(real_cost), "行动力": trader_active})
                                self.handle_event(info)
                                return self.immediate()

                    if self.m_objUser.m_nCurActive > active_config["limit"]["max_reserve"]:
                        for trader in info["商人们"]:
                            trader_active = int(trader["active"])
                            if trader_active > self.m_objUser.m_nCurActive:
                                continue
                            cost = trader["cost"].split(":")
                            real_cost = int(cost[1])
                            if cost[0] == "gold":
                                if real_cost <= active_config["limit"]["gold"] and real_cost <= self.get_available_gold():
                                    info = active_mgr.western_trade(trader["id"], {"金币": real_cost, "行动力": trader_active})
                                    self.handle_event(info)
                                    return self.immediate()
                            elif cost[0] == "copper":
                                if real_cost <= active_config["limit"]["copper"]:
                                    if real_cost > self.get_available_copper():
                                        misc_mgr.get_tickets_reward_by_name("银币", 10)
                                    info = active_mgr.western_trade(trader, {"银币": GlobalFunc.get_short_readable(real_cost), "行动力": trader_active})
                                    self.handle_event(info)
                                    return self.immediate()

        return self.next_half_hour()

    def handle_event(self, info):
        if info is None:
            return
        active_mgr = self.m_objServiceFactory.get_active_mgr()
        active_config = config["active"]["caravan"]["event"][info["事件"]]
        if info["事件"] == "1":
            is_double = 0
            if info["可领取状态"]:
                active_mgr.get_king_reward(is_double, info["位置"], info["双倍奖励消耗金币"])
            else:
                if info["双倍奖励消耗金币"] <= active_config["double_cost"] and info["双倍奖励消耗金币"] <= self.get_available_gold():
                    is_double = 1
                else:
                    is_double = -1
                active_mgr.get_king_reward(is_double, info["位置"], info["双倍奖励消耗金币"])
        elif info["事件"] == "2":
            for index, status in enumerate(info["可领取状态"]):
                cost = info["消耗金币"][index]
                if status == "1" and cost <= active_config["use_cost"] and cost <= self.get_available_gold():
                    active_mgr.get_trader_reward(index + 1, cost)
            active_mgr.get_trader_reward(-1, 0)

        elif info["事件"] == "3":
            is_double = 0
            if info["双倍奖励消耗金币"] <= active_config["double_cost"] and info["双倍奖励消耗金币"] <= self.get_available_gold():
                is_double = 1
            active_mgr.get_western_trade_reward(is_double, info["双倍奖励消耗金币"])
