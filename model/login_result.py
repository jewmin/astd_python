# -*- coding: utf-8 -*-
# 登录结果
from model.enum.login_status import LoginStatus


class LoginResult(object):
    def __init__(self):
        super(LoginResult, self).__init__()
        self.m_eLoginStatus = None
        self.m_szGameUrl = None
        self.m_szJSessionId = None
        self.m_dictCookies = None

    def get_login_status_desc(self):
        if self.m_eLoginStatus == LoginStatus.Success:
            return "登录成功"
        elif self.m_eLoginStatus == LoginStatus.NeedVerifyCode:
            return "需要输入验证码"
        elif self.m_eLoginStatus == LoginStatus.FailInGetToken:
            return "获取登录token失败, 请重试"
        elif self.m_eLoginStatus == LoginStatus.FailInLogin:
            return "登录失败, 请检查是否用户名/密码错误"
        elif self.m_eLoginStatus == LoginStatus.FailInGetServerList:
            return "获取服务器列表失败"
        elif self.m_eLoginStatus == LoginStatus.FailInFindingGameUrl:
            return "获取游戏地址失败"
        elif self.m_eLoginStatus == LoginStatus.FailInGoToGameUrl:
            return "跳转到游戏地址失败, 请查看是否已经合区"
        elif self.m_eLoginStatus == LoginStatus.FailInGetSession:
            return "获取会话失败"
        else:
            return "未知登录错误"