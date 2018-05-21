# -*- coding: utf-8 -*-
# 日常任务
from model.base_object import BaseObject


class Task(BaseObject):
    def __init__(self):
        super(Task, self).__init__()
        self.taskstate = 0
        self.finishnum = 0
        self.finishline = 0
        self.taskname = ""
        self.content = ""
        self.type = 0
