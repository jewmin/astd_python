# -*- coding: utf-8 -*-
# 要玩登录
import re
from requests.cookies import RequestsCookieJar
from login.login_base import LoginBase
from model.login_result import LoginResult
from manager.transfer_mgr import TransferMgr
from model.enum.login_status import LoginStatus


class YaoWanLogin(LoginBase):
    def __init__(self):
        super().__init__()

    async def login(self, cookies:RequestsCookieJar, verify=None, extra=None) -> LoginResult:
        self.logging()
        login_result = LoginResult()
        url = "http://www.yaowan.com/?m=user&action=loginform&subdomain=as"
        data = {"username": self.m_szUserName, "password": self.m_szPassword}
        response = await TransferMgr.post_pure(url, data, cookies)
        if response is None:
            login_result.m_eLoginStatus = LoginStatus.FailInLogin
        else:
            content = await response.text()
            if content.startswith("<script>"):
                login_result.m_eLoginStatus = LoginStatus.FailInLogin
            else:
                self.finding_server_url()
                server_url = await self.get_server_url(cookies)
                if server_url is None:
                    login_result.m_eLoginStatus = LoginStatus.FailInFindingGameUrl
                else:
                    await self.process_redirect(server_url, login_result, cookies)
        return login_result

    async def get_server_url(self, cookies:RequestsCookieJar) -> str:
        url = "http://as.yaowan.com/as_server_list.html"
        file_name = "yao_wan_as_server_list.html"
        content = self.get_cache_file(file_name)
        if len(content) == 0:
            return await self.get_and_save_url(url, cookies, file_name)
        else:
            game_url = self.find_server_url_from_string(content)
            if len(game_url) > 0:
                return game_url
            else:
                return await self.get_and_save_url(url, cookies, file_name)

    async def get_and_save_url(self, url:str, cookies:RequestsCookieJar, file_name:str):
        response = await TransferMgr.get_pure(url, cookies)
        if response is None:
            return ""
        else:
            content = await response.text()
            game_url = self.find_server_url_from_string(content)
            if len(game_url) > 0:
                self.save_cache_file(file_name, content)
                return game_url
            else:
                return ""

    def find_server_url_from_string(self, content:str) -> str:
        if self.m_objAccount.m_nServerId == 218 or self.m_objAccount.m_nServerId == 219:
            name = f"要玩{self.m_objAccount.m_nServerId}区"
        elif self.m_objAccount.m_nServerId == 272:
            name = "傲视争霸区"
        elif self.m_objAccount.m_nServerId == 470:
            name = "CJ专属服"
        elif self.m_objAccount.m_nServerId == 500:
            name = "虎贲营"
        elif self.m_objAccount.m_nServerId == 1000:
            name = "龍"
        else:
            name = f"双线{self.m_objAccount.m_nServerId}区"
        compiler = re.compile(f"<a.*href=\"(.*?)\".*>({name}.*)</a>")
        search = re.search(compiler, content)
        if search is None:
            return ""
        match = search.groups()
        if match is None or len(match) < 2:
            return ""
        else:
            return match[0]
