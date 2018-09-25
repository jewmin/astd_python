# -*- coding: utf-8 -*-
# 群雄争霸
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType


class KFZB(ActivityTask):
    def __init__(self):
        super(KFZB, self).__init__(ActivityType.GoldBoxEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "群雄争霸"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_match_detail()
        if info is None:
            return self.ten_minute()

        # goods = self.get_kfzb_market()
        # if goods is None:
        #     return self.next_half_hour()

        if info["可以鼓舞"] and info["鼓舞花费金币"] <= 0:
            if int(info["攻方"]["playerlevel"]) >= int(info["守方"]["playerlevel"]):
                self.support(info["攻方"], info["鼓舞花费金币"])
            else:
                self.support(info["守方"], info["鼓舞花费金币"])
            return self.immediate()
        else:
            return self.one_minute()

    def get_match_detail(self):
        url = "/root/kfzb!getMatchDetail.action"
        result = self.get_xml(url, "群雄争霸")
        if result and result.m_bSucceed:
            info = dict()
            info["攻方"] = result.m_objResult["message"].get("attacker", None)
            info["守方"] = result.m_objResult["message"].get("defender", None)
            info["可以鼓舞"] = result.m_objResult["message"].get("canbuymorereward", "0") == "1"
            info["鼓舞花费金币"] = int(result.m_objResult["message"].get("buymorerewardgold", "0"))
            return info

    def support(self, competitor, cost):
        url = "/root/kfzb!support.action"
        data = {"competitorId": competitor["competitorid"]}
        result = self.post_xml(url, data, "支持")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            if cost == 0:
                self.info("免费支持[{}]".format(competitor["playername"]))
            else:
                self.info("花费{}金币，支持[{}]".format(cost, competitor["playername"]), True)

    def get_kfzb_market(self):
        url = "/root/kfzb!getKfzbMarket.action"
        result = self.get_xml(url, "争霸商城")
        if result and result.m_bSucceed:
            goods = dict()
            goods["冷却时间"] = int(result.m_objResult["message"]["nextcd"])
            goods["商品"] = result.m_objResult["message"].get("kfzbshop", [])
            return goods

    def buy_from_kfzb_market(self, market):
        url = "/root/kfzb!buyFromKfzbMarket.action"
        data = {"marketId": market["marketid"]}
        result = self.post_xml(url, data, "购买商品")
        if result and result.m_bSucceed:
            pass
