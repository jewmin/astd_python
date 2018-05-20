# -*- coding: utf-8 -*-
# 专属玉佩
from model.base_object import BaseObject


class SpecialTreasure(BaseObject):
    def __init__(self):
        super(SpecialTreasure, self).__init__()
        self.storeid = 0
        self.upgradestate = 0
        self.consecratestatus = 0
        self.generalname = ""
        self.attribute_lea = 0
        self.attribute_str = 0
        self.attribute_int = 0
        self.additionalattributelvmax = 0
        self.maxadd = 0
        self.quality = 0
        self.name = ""
        self.succprob = 0.0
