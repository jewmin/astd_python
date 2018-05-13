# -*- coding: utf-8 -*-
# 祭祀
from model.base_object import BaseObject


class Fete(BaseObject):
    def __init__(self):
        super(Fete, self).__init__()
        self.id = 0
        self.gold = 0
        self.name = ""
