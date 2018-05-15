# -*- coding: utf-8 -*-
# 登录服务器类型
from enum import Enum, unique


@unique
class ServerType(Enum):
    YaoWan = 1  # 要玩
    PeiYou = 2  # 陪游


class ServerTypeString(object):
    @staticmethod
    def get_desc(server_type):
        if ServerType.YaoWan == server_type:
            return "要玩"
        elif ServerType.PeiYou == server_type:
            return "陪游"
        else:
            return str(server_type)
