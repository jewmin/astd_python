# -*- coding: utf-8 -*-
# 登录管理
from model.enum.server_type import ServerType
from login.impl.yaowan_login_impl import YaoWanLogin


class LoginMgr(object):
    def __init__(self):
        pass

    def get_login_impl(self, server_type):
        if server_type == ServerType.YaoWan:
            return YaoWanLogin()
        else:
            raise NotImplementedError

    def login(self, account, cookies, verify=None, extra=None):
        if account is None:
            return None
        else:
            partner = self.get_login_impl(account.m_eServerType)
            return partner.login(cookies, verify, extra)
