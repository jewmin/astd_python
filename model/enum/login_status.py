# -*- coding: utf-8 -*-
# 登录状态
from enum import Enum, unique


@unique
class LoginStatus(Enum):
    Success              = 0    # 成功
    NeedVerifyCode       = 1    # 需要验证码
    FailInGetToken       = 2    # 获取token失败
    FailInLogin          = 3    # 登录失败
    FailInGetServerList  = 4    # 获取服务器列表失败
    FailInFindingGameUrl = 5    # 获取游戏url失败
    FailInGoToGameUrl    = 6    # 跳转到游戏url失败
    FailInGetSession     = 7    # 获取session失败
    Unknown              = 100  # 未知错误


class LoginStatusString:
    descriptions = {
        LoginStatus.Unknown: "未知登录错误",
        LoginStatus.Success: "登录成功",
        LoginStatus.NeedVerifyCode: "需要输入验证码",
        LoginStatus.FailInGetToken: "获取登录token失败, 请重试",
        LoginStatus.FailInLogin: "登录失败, 请检查是否用户名/密码错误",
        LoginStatus.FailInGetServerList: "获取服务器列表失败",
        LoginStatus.FailInFindingGameUrl: "获取游戏地址失败",
        LoginStatus.FailInGoToGameUrl: "跳转到游戏地址失败, 请查看是否已经合区",
        LoginStatus.FailInGetSession: "获取会话失败",
    }

    @staticmethod
    def get(login_status:LoginStatus) -> str:
        return LoginStatusString.descriptions.get(login_status)
