# -*- coding: utf-8 -*-
# 集市商品
from model.base_object import BaseObject


class SupperMarketDto(BaseObject):
    def __init__(self):
        super(SupperMarketDto, self).__init__()
        self.id = 0
        self.price = 0
        self.name = ""
        self.num = 0
        self.baoshinum = 0
        self.finalprice = 0

    def get_price(self):
        res = self.price.split(":")
        return res[1], res[2]


class SupperMarketSpecialDto(BaseObject):
    def __init__(self):
        super(SupperMarketSpecialDto, self).__init__()
        self.id = 0
        self.price = 0
        self.itemname = ""
        self.num = 0
        self.state = 0

    def get_price(self):
        res = self.price.split(":")
        return res[1], res[2]
