# -*- coding: utf-8 -*-
# 主城建筑
from model.base_object import BaseObject


class MainCityDto(BaseObject):
    def __init__(self):
        super(MainCityDto, self).__init__()
        self.id = 0
        self.buildid = 0
        self.buildname = ""
        self.buildlevel = 0
        self.nextcopper = 0
        self.cdtime = 0
