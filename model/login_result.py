# -*- coding: utf-8 -*-
# 登录结果


class LoginResult(object):
    def __init__(self):
        super(LoginResult, self).__init__()
        self.m_eLoginStatus = None
        self.m_szGameUrl = None
        self.m_szJSessionId = None
        self.m_dictCookies = None
