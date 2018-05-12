# -*- coding: utf-8 -*-
# 将军塔
from model.base_object import BaseObject


class GeneralTower(BaseObject):
    def __init__(self):
        super(GeneralTower, self).__init__()
        self.buildingprogress = 0
        self.leveluprequirement = 0
        self.buildingstone = 0
        self.gemstonenum = 0
        self.generaltowerlevel = 0
        self.addprogress = 0
        self.levelup = 0
