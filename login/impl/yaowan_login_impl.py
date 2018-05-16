# -*- coding: utf-8 -*-
# 要玩登录
from logging import getLogger
import re
from login.login_base import LoginBase
from manager.transfer_mgr import TransferMgr
from model.login_result import LoginResult
from model.enum.login_status import LoginStatus


class YaoWanLogin(LoginBase):
    def __init__(self, index):
        super(YaoWanLogin, self).__init__(index)
        self.logger = getLogger(index)

    def login(self, cookies, verify=None, extra=None):
        self.logging()
        login_result = LoginResult()
        url = "http://www.yaowan.com/?m=user&action=loginform&subdomain=as"
        data = {"username": self.m_szUserName, "password": self.m_szPassword}
        result = TransferMgr.post_pure(url, data, cookies)
        if result is None:
            login_result.m_eLoginStatus = LoginStatus.FailInLogin
        elif result.content.startswith("<script>"):
            login_result.m_eLoginStatus = LoginStatus.FailInLogin
        else:
            self.finding_server_url()
            server_url = self.get_server_url(cookies)
            if server_url is None:
                login_result.m_eLoginStatus = LoginStatus.FailInFindingGameUrl
            else:
                self.process_redirect(server_url, login_result, cookies)
        return login_result

    def get_server_url(self, cookies):
        url = "http://as.yaowan.com/as_server_list.html"
        file_name = "yao_wan_as_server_list.html"
        content = self.get_cache_file(file_name)
        if len(content) == 0:
            return self.get_and_save_url(url, cookies, file_name)
        else:
            game_url = self.find_server_url_from_string(content)
            if len(game_url) > 0:
                return game_url
            else:
                return self.get_and_save_url(url, cookies, file_name)

    def get_and_save_url(self, url, cookies, file_name):
        result = TransferMgr.get_pure(url, cookies)
        if result is None:
            return ""
        else:
            content = result.content
            game_url = self.find_server_url_from_string(content)
            if len(game_url) > 0:
                self.save_cache_file(file_name, content)
                return game_url
            else:
                return ""

    def find_server_url_from_string(self, content):
        if self.m_objAccount.m_nServerId == 218 or self.m_objAccount.m_nServerId == 219:
            name = "要玩{}区".format(self.m_objAccount.m_nServerId)
        elif self.m_objAccount.m_nServerId == 272:
            name = "傲视争霸区"
        elif self.m_objAccount.m_nServerId == 470:
            name = "CJ专属服"
        elif self.m_objAccount.m_nServerId == 500:
            name = "虎贲营"
        elif self.m_objAccount.m_nServerId == 1000:
            name = "龍"
        else:
            name = "双线{}区".format(self.m_objAccount.m_nServerId)
        compiler = re.compile("<a.*href=\"(.*?)\".*>({}.*)</a>".format(name))
        search = re.search(compiler, content)
        if search is None:
            return ""
        match = search.groups()
        if match is None or len(match) < 2:
            return ""
        else:
            return match[0]
