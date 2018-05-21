# -*- coding: utf-8 -*-
# 行动力管理
from manager.base_mgr import BaseMgr
from model.reward_info import RewardInfo
from model.global_func import GlobalFunc


class ActiveMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(ActiveMgr, self).__init__(time_mgr, service_factory, user, index)

    #######################################
    # caravan begin
    #######################################
    def get_western_trade_info(self):
        url = "/root/caravan!getWesternTradeInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "西域通商")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["商人们"] = result.m_objResult["tradeinfo"]
            dict_info["进入下一站"] = result.m_objResult.get("needclicknext", "0") == "1"
            event_type = result.m_objResult.get("eventtype", "0")
            if event_type != "0":
                self.handle_western_trade_event(event_type, dict_info, result.m_objResult)
            return dict_info

    def handle_western_trade_event(self, event_type, dict_info, result):
        dict_info["事件"] = event_type
        if event_type == "1":
            dict_info["双倍奖励消耗金币"] = int(result["doublecost"])
            dict_info["可领取状态"] = result["firststatus"] != "2" and result["secondstatus"] != "2"
            dict_info["位置"] = 0
            num = 0
            msg = "西域国王宝箱[ "
            for index, v in enumerate(result["box"]):
                reward_info = RewardInfo()
                reward_info.handle_info(v["rewardinfo"])
                msg += "{} ".format(reward_info)
                reward = reward_info.get_reward(0)
                if reward is not None and reward.num > num:
                    dict_info["位置"] = index
                    num = reward.num
            msg += "]"
        elif event_type == "2":
            dict_info["可领取状态"] = [result["firststatus"], result["secondstatus"]]
            dict_info["消耗金币"] = list()
            msg = "神秘商人宝箱[ "
            for index, v in enumerate(result["box"]):
                dict_info["消耗金币"].append(int(v["cost"]))
                msg += "宝箱[花费{}金币] ".format(v["cost"])
            msg += "]"
        elif event_type == "3":
            dict_info["双倍奖励消耗金币"] = int(result["doublecost"])
            msg = "西域通商宝箱[ "
            for v in result["box"]:
                reward_info = RewardInfo()
                reward_info.handle_info(v["rewardinfo"])
                msg += "{} ".format(reward_info)
            msg += "]"
        self.info(msg)

    def get_king_reward(self, is_double, pos, cost):
        url = "/root/caravan!getKingReward.action"
        data = {"isdouble": is_double, "pos": pos}
        result = self.get_protocol_mgr().post_xml(url, data, "西域国王")
        if result and result.m_bSucceed:
            use_gold = False
            if is_double == -1:
                msg = "取消领取西域国王奖励"
            else:
                reward_info = RewardInfo()
                reward_info.handle_info(result.m_objResult["rewardinfo"])
                msg = "领取西域国王奖励"
                if is_double > 0:
                    use_gold = True
                    msg = "花费{}金币，领取双倍西域国王奖励".format(cost)
                msg += "，获得{}".format(reward_info)
            self.info(msg, use_gold)

    def get_trader_reward(self, is_buy, cost):
        url = "/root/caravan!getTraderReward.action"
        data = {"isBuy": is_buy}
        result = self.get_protocol_mgr().post_xml(url, data, "神秘商人")
        if result and result.m_bSucceed:
            use_gold = False
            if is_buy == -1:
                msg = "取消购买神秘商人宝箱"
            else:
                if cost > 0:
                    use_gold = True
                msg = "花费{}金币购买神秘商人宝箱，获得".format(cost)
            self.info(msg, use_gold)

    def next_place(self):
        url = "/root/caravan!nextPlace.action"
        result = self.get_protocol_mgr().get_xml(url, "下一站")
        if result and result.m_bSucceed:
            self.info("进入下一站")

    def western_trade(self, trader, cost):
        url = "/root/caravan!westernTrade.action"
        data = {"tradeId": trader["id"]}
        result = self.get_protocol_mgr().post_xml(url, data, "通商")
        if result and result.m_bSucceed:
            use_gold = False
            msg = "花费"
            first = True
            for k, v in cost.iteritems():
                if k == "金币":
                    use_gold = True
                if first:
                    first = False
                    msg += "{}{}".format(v, k)
                else:
                    msg += "、{}{}".format(v, k)
            msg += "通商[{}]".format(trader["name"])
            self.info(msg, use_gold)

            dict_info = dict()
            event_type = result.m_objResult.get("eventtype", "0")
            if event_type != "0":
                self.handle_western_trade_event(event_type, dict_info, result.m_objResult)
            return dict_info

    def get_western_trade_reward(self, is_double, cost):
        url = "/root/caravan!getWesternTradeReward.action"
        data = {"isdouble": is_double}
        result = self.get_protocol_mgr().post_xml(url, data, "通商奖励")
        if result and result.m_bSucceed:
            use_gold = False
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            msg = "领取通商奖励"
            if is_double > 0:
                use_gold = True
                msg = "花费{}金币，领取双倍通商奖励".format(cost)
            msg += "，获得{}".format(reward_info)
            self.info(msg, use_gold)

    #######################################
    # refine begin
    #######################################
    def get_refine_bin_tie_factory(self):
        url = "/root/refine!getRefineBintieFactory.action"
        result = self.get_protocol_mgr().get_xml(url, "高级炼制工坊")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["行动力状态"] = int(result.m_objResult["status"])
            dict_info["消耗银币"] = int(result.m_objResult["coppercost"])
            dict_info["消耗行动力"] = int(result.m_objResult["needactive"])
            dict_info["剩余高效次数"] = int(result.m_objResult["remainhigh"])
            dict_info["剩余极限次数"] = int(result.m_objResult["remainlimit"])
            dict_info["极限次数"] = int(result.m_objResult["limit"])
            self.info("可炼制次数({}/{})".format(dict_info["剩余极限次数"], dict_info["极限次数"]))
            return dict_info

    def do_refine_bin_tie_factory(self, copper, active, mode):
        url = "/root/refine!doRefineBintieFactory.action"
        data = {"mode": mode}
        result = self.get_protocol_mgr().post_xml(url, data, "炼制")
        if result and result.m_bSucceed:
            self.add_task_finish_num(10, 1)
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("消耗{}银币、{}行动力炼制，获得{}".format(GlobalFunc.get_short_readable(copper), active, reward_info))

    def get_refine_info(self):
        url = "/root/refine!getRefineInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "精炼工房")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["行动力状态"] = int(result.m_objResult["status"])
            dict_info["消耗银币"] = int(result.m_objResult["copper"])
            dict_info["消耗行动力"] = int(result.m_objResult["needactive"])
            dict_info["剩余高效次数"] = int(result.m_objResult["remainhigh"])
            dict_info["剩余极限次数"] = int(result.m_objResult["remainlimit"])
            dict_info["极限次数"] = int(result.m_objResult["limit"])
            dict_info["消耗余料"] = int(result.m_objResult["onceplus"])
            dict_info["当前余料"] = int(result.m_objResult["refinenum"])
            dict_info["余料上限"] = int(result.m_objResult["maxrefinenum"])
            dict_info["升级单个工人消耗金币"] = int(result.m_objResult["percost"])
            dict_info["工人们"] = result.m_objResult["refiner"]
            dict_info["可精炼工人"] = False
            for v in result.m_objResult["refinergroup"]:
                if v["time"] == "0":
                    dict_info["可精炼工人"] = True
                    break
            self.info("余料库存({}/{})，可精炼次数({}/{})".format(dict_info["当前余料"], dict_info["余料上限"], dict_info["剩余极限次数"], dict_info["极限次数"]))
            return dict_info

    def refine(self, copper, active):
        url = "/root/refine!refine.action"
        result = self.get_protocol_mgr().get_xml(url, "精炼")
        if result and result.m_bSucceed:
            self.add_task_finish_num(9, 1)
            msg = "消耗{}银币、{}行动力精炼".format(copper, active)
            if "eventintro" in result.m_objResult:
                msg += "，触发精炼事件<{}>".format(result.m_objResult["eventintro"])
            bao_ji = int(result.m_objResult["baoji"])
            if bao_ji > 0:
                msg += "，{}倍暴击".format(bao_ji)
            msg += "，获得{}玉石".format(result.m_objResult["bowlder"])
            if "baoshi" in result.m_objResult:
                msg += "，{}宝石".format(result.m_objResult["baoshi"])
            self.info(msg)

    def refresh_one_refiner(self, refiner, cost):
        url = "/root/refine!refreshOneRefiner.action"
        data = {"refinerOrder": refiner["order"]}
        result = self.get_protocol_mgr().post_xml(url, data, "升级精炼工人")
        if result and result.m_bSucceed:
            use_gold = False
            if cost > 0:
                use_gold = True
            self.info("花费{}金币升级精炼工人[{}({})]".format(cost, refiner["name"], refiner["color"]), use_gold)

    #######################################
    # make begin
    #######################################
    def royalty_weave_info2(self):
        url = "/root/make!royaltyWeaveInfo2.action"
        result = self.get_protocol_mgr().get_xml(url, "御用精纺厂")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["行动力状态"] = int(result.m_objResult["activestatus"])
            dict_info["消耗行动力"] = int(result.m_objResult["needactive"])
            dict_info["剩余高效次数"] = int(result.m_objResult["remainhigh"])
            dict_info["高效次数"] = int(result.m_objResult["high"])
            dict_info["剩余极限次数"] = int(result.m_objResult["remainlimit"])
            dict_info["极限次数"] = int(result.m_objResult["limit"])
            dict_info["布匹"] = int(result.m_objResult["weavenum"])
            dict_info["布匹上限"] = int(result.m_objResult["maxnum"])
            dict_info["换购消耗布匹"] = int(result.m_objResult["needweavenum"])
            dict_info["商人"] = result.m_objResult["tradername"]
            dict_info["刷新商人费用"] = int(result.m_objResult["cost"])
            dict_info["换购商品"] = RewardInfo()
            dict_info["换购商品"].handle_info(result.m_objResult["rewardinfo"])
            self.info("布匹({}/{})，商人({}，可换购{})，可纺织次数({}/{})".format(
                dict_info["布匹"], dict_info["布匹上限"], dict_info["商人"], dict_info["换购商品"],
                dict_info["剩余极限次数"], dict_info["极限次数"]))
            return dict_info

    def royalty_weave2(self, active, times):
        url = "/root/make!royaltyWeave2.action"
        data = {"times": times}
        result = self.get_protocol_mgr().post_xml(url, data, "一键纺织")
        if result and result.m_bSucceed:
            self.add_task_finish_num(12, times)
            msg = "花费{}行动力一键纺织".format(active)
            once_num = int(result.m_objResult["oncenum"])
            bu_pi = result.m_objResult["bupi"]
            if isinstance(bu_pi, list):
                for v in bu_pi:
                    msg += "，布匹+{}".format(int(v["modulus"]) * once_num)
            else:
                msg += "，布匹+{}".format(int(bu_pi["modulus"]) * once_num)
            self.info(msg)

    def convert_royalty_weave_new2(self, need_weave_num):
        url = "/root/make!convertRoyaltyWeaveNew2.action"
        result = self.get_protocol_mgr().get_xml(url, "换购")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("花费{}布匹换购，获得{}".format(need_weave_num, reward_info))

    def refresh_royalty_weave_new(self, cost):
        url = "/root/make!refreshRoyaltyWeaveNew.action"
        result = self.get_protocol_mgr().get_xml(url, "刷新换购商人")
        if result and result.m_bSucceed:
            use_gold = False
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            if cost > 0:
                use_gold = True
            self.info("花费{}金币刷新换购商人，商人({}，可换购{})".format(cost, result.m_objResult["tradername"], reward_info), use_gold)
