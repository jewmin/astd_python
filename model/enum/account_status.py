# -*- coding: utf-8 -*-
# 账号状态
from enum import Enum, unique


@unique
class AccountStatus(Enum):
    NotStart = 0  # 挂机未运行
    Initial = 1  # 初始化
    Running = 2  # 挂机运行中
    ReLogin = 3  # 等待重登录
    Stopped = 4  # 挂机停止中
    StoppedLoginVerify = 5  # 等待登录验证码
    LoginFailed = 6  # 登录失败
    LoginFailedMax = 7  # 达到最大登录次数
    StoppedGameVerify = 8  # 等待游戏验证码
    DueTime = 100  # 已过期
