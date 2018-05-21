# -*- coding: utf-8 -*-
# 建筑建造队列
from model.base_object import BaseObject


class ConstructorDto(BaseObject):
    def __init__(self):
        super(ConstructorDto, self).__init__()
        self.cid = 0
        self.cdflag = 0
        self.ctime = 0
