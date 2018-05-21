# -*- coding: utf-8 -*-
# 登录状态
from enum import Enum, unique


@unique
class LoginStatus(Enum):
    Success = 0  # 成功
    NeedVerifyCode = 1  # 需要验证码
    FailInGetToken = 2  # 获取token失败
    FailInLogin = 3  # 登录失败
    FailInGetServerList = 4  # 获取服务器列表失败
    FailInFindingGameUrl = 5  # 获取游戏url失败
    FailInGoToGameUrl = 6  # 跳转到游戏url失败
    FailInGetSession = 7  # 获取session失败
