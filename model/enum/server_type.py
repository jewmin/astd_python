# -*- coding: utf-8 -*-
# 登录渠道类型
from enum import Enum, unique


@unique
class ServerType(Enum):
    YaoWan  = 1    # 要玩
    PeiYou  = 2    # 陪游
    Unknown = 100  # 未知渠道


class ServerTypeString:
    descriptions = {
        ServerType.Unknown: "未知渠道",
        ServerType.YaoWan: "要玩",
        ServerType.PeiYou: "陪游",
    }

    @staticmethod
    def get(server_type:ServerType) -> str:
        return ServerTypeString.descriptions.get(server_type)
