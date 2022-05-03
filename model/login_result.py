# -*- coding: utf-8 -*-
# 登录结果
from requests.cookies import RequestsCookieJar
from model.enum.login_status import LoginStatus, LoginStatusString


class LoginResult:
    def __init__(self):
        self.m_eLoginStatus = LoginStatus.Unknown
        self.m_szGameUrl = ''
        self.m_szJSessionId = ''
        self.m_dictCookies = RequestsCookieJar()

    def __str__(self) -> str:
        return LoginStatusString.get(self.m_eLoginStatus)
