# -*- coding: utf-8 -*-
# 百炼精铁
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType


class ShenHuo(ActivityTask):
    def __init__(self):
        super(ShenHuo, self).__init__(ActivityType.ShenHuo)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "百炼精铁"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_info()
        if info is None:
            return self.next_half_hour()

        if info["预计累计精纯度"] == 0:
            self.start()
            return self.immediate()

        return self.next_half_hour()

    def get_info(self):
        url = "/root/shenhuo!getInfo.action"
        result = self.get_xml(url, "百炼精铁")
        if result and result.m_bSucceed:
            info = dict()
            info["预计累计精纯度"] = int(result.m_objResult["preshenhuochundu"])
            return info

    def start(self):
        url = "/root/shenhuo!start.action"
        result = self.get_xml(url, "百炼精铁")
        if result and result.m_bSucceed:
            self.info("开始百炼精铁")
