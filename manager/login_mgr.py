# -*- coding: utf-8 -*-
# 登录管理
from model.enum.server_type import ServerType
from login.impl.yaowan_login_impl import YaoWanLogin


class LoginMgr(object):
    def __init__(self, index):
        super(LoginMgr, self).__init__()
        self.m_szIndex = index

    def get_login_impl(self, server_type):
        if server_type == ServerType.YaoWan:
            return YaoWanLogin(self.m_szIndex)
        else:
            raise NotImplementedError

    def login(self, account, cookies, verify=None, extra=None):
        if account is not None:
            partner = self.get_login_impl(account.m_eServerType)
            partner.set_account(account)
            return partner.login(cookies, verify, extra)
