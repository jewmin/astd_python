# -*- coding: utf-8 -*-
# 登录基类
from logging import getLogger
import hashlib
from urlparse import urlparse
from threading import Lock
import os
from manager.transfer_mgr import TransferMgr
from model.enum.login_status import LoginStatus


class LoginBase(object):
    def __init__(self, index):
        super(LoginBase, self).__init__()
        self.logger = getLogger(index)
        self.m_szUserName = None
        self.m_szPassword = None
        self.m_szMd5Password = None
        self.m_szMd5PasswordLower = None
        self.m_objAccount = None
        self.lock = Lock()

    def set_account(self, account):
        self.m_objAccount = account
        self.m_szUserName = self.m_objAccount.m_szUserName
        self.m_szPassword = self.m_objAccount.m_szPassword
        self.m_szMd5Password = hashlib.md5(self.m_objAccount.m_szPassword).hexdigest()
        self.m_szMd5PasswordLower = self.m_szMd5Password.lower()

    def save_cache_file(self, file_name, file_content):
        self.lock.acquire()
        folder = "cache"
        if not os.path.exists(folder):
            os.mkdir(folder)
        fd = open("{}/{}".format(folder, file_name), "w+")
        fd.write(file_content)
        fd.close()
        self.lock.release()

    def get_cache_file(self, file_name):
        self.lock.acquire()
        folder = "cache"
        if not os.path.exists(folder):
            os.mkdir(folder)
        try:
            fd = open("{}/{}".format(folder, file_name), "r+")
            content = fd.read()
            fd.close()
        except IOError as ex:
            self.logger.error(str(ex))
            content = ""
        self.lock.release()
        return content

    def login(self, cookies, verify=None, extra=None):
        pass

    def process_redirect(self, redirect_url, login_result, cookies):
        self.going_to_game_url()
        result = TransferMgr.get_pure(redirect_url, cookies)
        if result is None:
            login_result.m_eLoginStatus = LoginStatus.FailInGoToGameUrl
        else:
            location = result.headers.get("location", None)
            if location is None:
                login_result.m_eLoginStatus = LoginStatus.FailInGetSession
                self.logger.error(result.text)
            else:
                location = LoginBase.make_sure_valid_url(redirect_url, location)
                if "start.action" not in location:
                    self.process_redirect(location, login_result, cookies)
                else:
                    self.process_start_game(location, login_result, cookies)

    def process_start_game(self, start_url, login_result, cookies):
        self.getting_session()
        result = TransferMgr.get_pure(start_url, cookies)
        self.handle_start_game(result, login_result, cookies)

    def post_start_game(self, start_url, data, login_result, cookies):
        self.getting_session()
        result = TransferMgr.post_pure(start_url, data, cookies)
        self.handle_start_game(result, login_result, cookies)

    def handle_start_game(self, result, login_result, cookies):
        if result is None:
            login_result.m_eLoginStatus = LoginStatus.FailInGetSession
        else:
            login_result.m_szGameUrl = result.headers["location"]
            login_result.m_szJSessionId = result.cookies["JSESSIONID"]
            login_result.m_dictCookies = cookies
            if login_result.m_szJSessionId is None or login_result.m_szJSessionId == "":
                login_result.m_eLoginStatus = LoginStatus.FailInGetSession
            else:
                login_result.m_eLoginStatus = LoginStatus.Success
            self.succeed()

    @staticmethod
    def make_sure_valid_url(base_url, now_url):
        if now_url.startswith("http://") or now_url.startswith("https://"):
            return now_url
        else:
            result = urlparse(base_url)
            scheme = result.scheme
            netloc = result.netloc
            path = result.path
            index = path.rfind("/")
            if index >= 0:
                path = path[:index]
            if now_url.startswith("./"):
                now_url = now_url[1:]
            elif now_url.startswith("../"):
                now_url = now_url[2:]
                index = path.rfind("/")
                if index >= 0:
                    path = path[:index]
            elif now_url.startswith("/"):
                path = ""
            else:
                now_url = "/{}".format(now_url)
            return "{}://{}{}{}".format(scheme, netloc, path, now_url)

    def logging(self):
        self.send_status("正在登录...")

    def finding_server_url(self):
        self.send_status("正在获取所在区的地址...")

    def going_to_game_url(self):
        self.send_status("正在跳转到所在区地址...")

    def getting_session(self):
        self.send_status("正在获取会话...")

    def succeed(self):
        self.send_status("登录完成~~")

    def send_status(self, status):
        self.logger.info(status)
