# -*- coding: utf-8 -*-
# 账号信息
from requests.cookies import RequestsCookieJar
from model.enum.server_type import ServerType
from model.enum.account_status import AccountStatus


class Account:
    def __init__(self):
        self.m_eServerType = ServerType.Unknown
        self.m_nServerId = 0
        self.m_szUserName = ''
        self.m_szPassword = ''
        self.m_szRoleName = ''
        self.m_eAccountStatus = AccountStatus.DueTime
        self.m_szGameUrl = ''
        self.m_szJSessionId = ''
        self.m_distCookies = RequestsCookieJar()
