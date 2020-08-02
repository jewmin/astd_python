# -*- coding: utf-8 -*-
# 集市任务
from logic.base_task import BaseTask
from logic.config import config


class SupperMarketTask(BaseTask):
    def __init__(self):
        super(SupperMarketTask, self).__init__()
        self.m_szName = "suppermarket"
        self.m_szReadable = "集市"

    def run(self):
        if config["market"]["auto_buy_item"]:
            misc_mgr = self.m_objServiceFactory.get_misc_mgr()
            misc_mgr.bargain_supper_market_commodity(-1)
            supper_market_dto_set, supper_market_special_dto_set, fresh_time, supplement_num = misc_mgr.get_player_supper_market()
            with_draw_supper_market_dto_set = set()
            if config["market"]["withdraw_gold_item"]:
                for v in supper_market_dto_set:
                    price_type, price = v.get_price()
                    if price_type == "gold":
                        if v.name in config["market"]["withdraw_gold_item_exclude"]:
                            if v.quality >= config["market"]["withdraw_gold_item_exclude"][v.name]:
                                continue
                        misc_mgr.off_supper_market_commodity(v)
                        with_draw_supper_market_dto_set.add(v)
            supper_market_dto_set -= with_draw_supper_market_dto_set

            with_draw_supper_market_dto_set = set()
            config_withdraw_discount_fail = config["market"]["withdraw_discount_fail"]
            if config_withdraw_discount_fail["enable"]:
                for v in supper_market_dto_set:
                    price_type, price = v.get_price()
                    if config_withdraw_discount_fail[price_type] and price > v.finalprice:
                        misc_mgr.off_supper_market_commodity(v)
                        with_draw_supper_market_dto_set.add(v)
            supper_market_dto_set -= with_draw_supper_market_dto_set

            with_draw_supper_market_dto_set = set()
            for v in supper_market_dto_set:
                price_type, price = v.get_price()
                if price_type == "copper":
                    if price > self.get_available_copper():
                        misc_mgr.get_tickets_reward_by_name("银币", 1)
                    misc_mgr.buy_supper_market_commodity(v)
                    with_draw_supper_market_dto_set.add(v)
                elif price_type == "gold" and config["market"]["buy_gold_item"]:
                    if price <= self.get_available_gold():
                        misc_mgr.buy_supper_market_commodity(v, True)
                        with_draw_supper_market_dto_set.add(v)
            supper_market_dto_set -= with_draw_supper_market_dto_set

            if config["market"]["supplement_item"]["enable"]:
                if supplement_num > 0 and len(supper_market_dto_set) <= config["market"]["supplement_item"]["limit"]:
                    misc_mgr.supplement_supper_market()
                    fresh_time = self.immediate()

            if config["market"]["buy_special_item"]:
                for v in supper_market_special_dto_set:
                    if v.state == 1:
                        price_type, price = v.get_price()
                        if price_type == "copper":
                            if price > self.get_available_copper():
                                misc_mgr.get_tickets_reward_by_name("银币", 1)
                            misc_mgr.buy_supper_market_special_goods(v)
                        elif price_type == "gold":
                            if price <= self.get_available_gold():
                                misc_mgr.buy_supper_market_special_goods(v, True)

            if fresh_time is not None:
                return fresh_time

        return self.next_half_hour()
