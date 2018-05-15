# -*- coding: utf-8 -*-
# 集市商品
from model.base_object import BaseObject
from model.global_func import GlobalFunc


class SupperMarketDto(BaseObject):
    def __init__(self):
        super(SupperMarketDto, self).__init__()
        self.id = 0
        self.price = ""
        self.name = ""
        self.num = 0
        self.baoshinum = 0
        self.finalprice = 0

    def get_price(self):
        res = self.price.split(":")
        return res[1], int(res[2])

    def is_discount(self):
        price_type, price = self.get_price()
        if price > self.finalprice:
            return True
        else:
            return False

    def __str__(self):
        price_type, price = self.get_price()
        return "[{}{}]({}{})".format(GlobalFunc.get_short_readable(self.baoshinum) if self.baoshinum > 0 else GlobalFunc.get_short_readable(self.num), self.name, GlobalFunc.get_short_readable(self.finalprice), "银币" if price_type == "copper" else "金币")


class SupperMarketSpecialDto(BaseObject):
    def __init__(self):
        super(SupperMarketSpecialDto, self).__init__()
        self.id = 0
        self.price = ""
        self.itemname = "宝石"
        self.num = 0
        self.state = 0

    def get_price(self):
        res = self.price.split(":")
        return res[1], int(res[2])

    def __str__(self):
        price_type, price = self.get_price()
        return "[{}+{}]({}{})".format(self.itemname, GlobalFunc.get_short_readable(self.num), GlobalFunc.get_short_readable(price), "银币" if price_type == "copper" else "金币")