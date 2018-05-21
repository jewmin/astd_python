# -*- coding: utf-8 -*-
# 墨子建筑
from model.base_object import BaseObject


class MoZiBuilding(BaseObject):
    def __init__(self):
        super(MoZiBuilding, self).__init__()
        self.id = 0
        self.buildid = 0
        self.slaves = 0
        self.process = 0
        self.state = 0
        self.totalprocess = 0
        self.seniorprocess = 0
        self.totalseniorprocess = 0
