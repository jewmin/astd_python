# -*- coding: utf-8 -*-
# 登录基类
import os
import hashlib
from logging import getLogger
from aiohttp import ClientResponse
from threading import Lock
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar
from model.account import Account
from model.login_result import LoginResult
from manager.transfer_mgr import TransferMgr
from model.enum.login_status import LoginStatus


class LoginBase:
    def __init__(self) -> None:
        self.logger = getLogger(self.__class__.__name__)
        self.m_szUserName = ''
        self.m_szPassword = ''
        self.m_szMd5Password = ''
        self.m_szMd5PasswordLower = ''
        self.m_objAccount = Account()
        self.lock = Lock()

    def set_account(self, account:Account) -> None:
        self.m_objAccount = account
        self.m_szUserName = self.m_objAccount.m_szUserName
        self.m_szPassword = self.m_objAccount.m_szPassword
        self.m_szMd5Password = hashlib.md5(self.m_objAccount.m_szPassword).hexdigest()
        self.m_szMd5PasswordLower = self.m_szMd5Password.lower()

    def save_cache_file(self, file_name:str, file_content:str) -> None:
        self.lock.acquire()
        folder = "cache"
        os.makedirs(folder, exist_ok=True)
        with open(f"{folder}/{file_name}", "w+", encoding="utf-8") as fd:
            fd.write(file_content)
        self.lock.release()

    def get_cache_file(self, file_name:str) -> str:
        self.lock.acquire()
        folder = "cache"
        os.makedirs(folder, exist_ok=True)
        try:
            with open(f"{folder}/{file_name}", "r+", encoding="utf-8") as fd:
                content = fd.read()
        except IOError as ex:
            self.logger.error("加载文件失败", exc_info=True)
            content = ""
        self.lock.release()
        return content

    async def login(self, cookies:RequestsCookieJar, verify=None, extra=None) -> LoginResult:
        raise NotImplementedError("子类必须实现")

    async def process_redirect(self, redirect_url:str, login_result:LoginResult, cookies:RequestsCookieJar) -> None:
        self.going_to_game_url()
        response = await TransferMgr.get_pure(redirect_url, cookies)
        if response is None:
            login_result.m_eLoginStatus = LoginStatus.FailInGoToGameUrl
        else:
            location = response.headers.get("location")
            if location is None:
                login_result.m_eLoginStatus = LoginStatus.FailInGetSession
                self.logger.error(await response.text())
            else:
                location = LoginBase.make_sure_valid_url(redirect_url, location)
                if "start.action" not in location:
                    await self.process_redirect(location, login_result, cookies)
                else:
                    await self.process_start_game(location, login_result, cookies)

    async def process_start_game(self, start_url:str, login_result:LoginResult, cookies:RequestsCookieJar) -> None:
        self.getting_session()
        response = await TransferMgr.get_pure(start_url, cookies)
        self.handle_start_game(response, login_result, cookies)

    def handle_start_game(self, response:ClientResponse, login_result:LoginResult, cookies:RequestsCookieJar) -> None:
        if response is None:
            login_result.m_eLoginStatus = LoginStatus.FailInGetSession
        else:
            login_result.m_szGameUrl = response.headers["location"]
            login_result.m_szJSessionId = response.cookies["JSESSIONID"]
            login_result.m_dictCookies = cookies
            if not login_result.m_szJSessionId:
                login_result.m_eLoginStatus = LoginStatus.FailInGetSession
            else:
                login_result.m_eLoginStatus = LoginStatus.Success
            self.succeed()

    @staticmethod
    def make_sure_valid_url(base_url:str, now_url:str) -> str:
        if now_url.startswith("http://") or now_url.startswith("https://"):
            return now_url
        else:
            result = urlparse(base_url)
            scheme = result.scheme
            netloc = result.netloc
            path = result.path
            if (index := path.rfind("/")) >= 0:
                path = path[:index]
            if now_url.startswith("./"):
                now_url = now_url[1:]
            elif now_url.startswith("../"):
                now_url = now_url[2:]
                if (index := path.rfind("/")) >= 0:
                    path = path[:index]
            elif now_url.startswith("/"):
                path = ""
            else:
                now_url = f"/{now_url}"
            return f"{scheme}://{netloc}{path}{now_url}"

    def logging(self) -> None:
        self.send_status("正在登录...")

    def finding_server_url(self) -> None:
        self.send_status("正在获取所在区的地址...")

    def going_to_game_url(self) -> None:
        self.send_status("正在跳转到所在区地址...")

    def getting_session(self) -> None:
        self.send_status("正在获取会话...")

    def succeed(self) -> None:
        self.send_status("登录完成~~")

    def send_status(self, status:str) -> None:
        self.logger.info(status)
