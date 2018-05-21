# -*- coding: utf-8 -*-
# 通用方法
from logic.config import config


class GlobalFunc(object):
    @staticmethod
    def get_short_readable(value):
        if value >= 10000:
            return "{}万".format(value / 10000)
        else:
            return value

    @staticmethod
    def get_available(key, value):
        reserve = config["global"]["reserve"].get(key, 0)
        return max(value - reserve, 0)
