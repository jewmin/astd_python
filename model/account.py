# -*- coding: utf-8 -*-
# 账号信息


class Account(object):
    def __init__(self):
        super(Account, self).__init__()
        self.m_eServerType = None
        self.m_nServerId = None
        self.m_szUserName = None
        self.m_szPassword = None
        self.m_szRoleName = None
        self.m_eAccountStatus = None
        self.m_szGameUrl = None
        self.m_szJSessionId = None
        self.m_distCookies = None
