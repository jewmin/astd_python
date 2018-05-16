# -*- coding: utf-8 -*-
# 行动力管理
from logging import getLogger
from manager.base_mgr import BaseMgr


class ActiveMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, index):
        super(ActiveMgr, self).__init__(time_mgr, service_factory)
        self.logger = getLogger(index)

    #######################################
    # caravan begin
    #######################################
    def get_western_trade_info(self):
        url = "/root/caravan!getWesternTradeInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "西域通商")
        if result and result.m_bSucceed:
            pass

    def get_king_reward(self, is_double, pos):
        url = "/root/caravan!getKingReward.action"
        data = {"isdouble": is_double, "pos": pos}
        result = self.get_protocol_mgr().post_xml(url, data, "西域国王")
        if result and result.m_bSucceed:
            pass

    def get_trader_reward(self, is_buy):
        url = "/root/caravan!getTraderReward.action"
        data = {"isBuy": is_buy}
        result = self.get_protocol_mgr().post_xml(url, data, "神秘商人")
        if result and result.m_bSucceed:
            pass

    def next_place(self):
        url = "/root/caravan!nextPlace.action"
        result = self.get_protocol_mgr().get_xml(url, "下一站")
        if result and result.m_bSucceed:
            pass

    def western_trade(self, trade_id):
        url = "/root/caravan!westernTrade.action"
        data = {"tradeId": trade_id}
        result = self.get_protocol_mgr().post_xml(url, data, "通商")
        if result and result.m_bSucceed:
            pass

    def get_western_trade_reward(self, is_double):
        url = "/root/caravan!getWesternTradeReward.action"
        data = {"isdouble": is_double}
        result = self.get_protocol_mgr().post_xml(url, data, "通商奖励")
        if result and result.m_bSucceed:
            pass

    #######################################
    # refine begin
    #######################################
    def get_refine_bin_tie_factory(self):
        url = "/root/refine!getRefineBintieFactory.action"
        result = self.get_protocol_mgr().get_xml(url, "高级炼制工坊")
        if result and result.m_bSucceed:
            pass

    def do_refine_bin_tie_factory(self, mode):
        url = "/root/refine!doRefineBintieFactory.action"
        data = {"mode": mode}
        result = self.get_protocol_mgr().post_xml(url, data, "炼制")
        if result and result.m_bSucceed:
            pass

    def get_refine_info(self):
        url = "/root/refine!getRefineInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "精炼工房")
        if result and result.m_bSucceed:
            pass

    def refine(self):
        url = "/root/refine!refine.action"
        result = self.get_protocol_mgr().get_xml(url, "精炼")
        if result and result.m_bSucceed:
            pass

    def refresh_one_refiner(self, refiner_order):
        url = "/root/refine!refreshOneRefiner.action"
        data = {"refinerOrder": refiner_order}
        result = self.get_protocol_mgr().post_xml(url, data, "升级精炼工人")
        if result and result.m_bSucceed:
            pass

    #######################################
    # make begin
    #######################################
    def royalty_weave_info2(self):
        url = "/root/make!royaltyWeaveInfo2.action"
        result = self.get_protocol_mgr().get_xml(url, "御用精纺厂")
        if result and result.m_bSucceed:
            pass

    def royalty_weave2(self, times):
        url = "/root/make!royaltyWeave2.action"
        data = {"times": times}
        result = self.get_protocol_mgr().post_xml(url, data, "一键纺织")
        if result and result.m_bSucceed:
            pass

    def convert_royalty_weave_new2(self):
        url = "/root/make!convertRoyaltyWeaveNew2.action"
        result = self.get_protocol_mgr().get_xml(url, "换购")
        if result and result.m_bSucceed:
            pass

    def refresh_royalty_weave_new(self):
        url = "/root/make!refreshRoyaltyWeaveNew.action"
        result = self.get_protocol_mgr().get_xml(url, "刷新换购商人")
        if result and result.m_bSucceed:
            pass
