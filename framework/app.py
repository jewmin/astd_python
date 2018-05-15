# -*- coding: utf-8 -*-
# 服务基类
from threading import Thread
from threading import Timer
import requests
import logging
from logging.handlers import TimedRotatingFileHandler
import time
import os
from framework.i_server import IServer
from manager.login_mgr import LoginMgr
from model.enum.login_status import LoginStatus
from model.enum.account_status import AccountStatus
from model.enum.server_type import ServerTypeString
from model.user import User
from manager.service_factory import ServiceFactory
from manager.task_mgr import TaskMgr
from manager.protocol_mgr import ProtocolMgr
from logic.common_task import CommonTask
from logic.fete_task import FeteTask
from logic.impose_task import ImposeTask
from logic.ticket_task import TicketTask
from logic.supper_market_task import SupperMarketTask


class App(IServer):
    def __init__(self, account_list):
        super(App, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.m_bServerRunning = False
        self.m_bIsReLogin = False
        self.m_threadTask = None
        self.m_timerReLogin = None
        self.m_objTaskMgr = None
        self.m_listAccounts = account_list
        self.m_objAccount = None
        self.m_objUser = None
        self.m_objServiceFactory = None
        self.m_objProtocolMgr = None
        self.m_objTaskMgr = None

    def init(self, user_name, role_name):
        for account in self.m_listAccounts:
            if account.m_szUserName == user_name and account.m_szRoleName == role_name:
                self.m_objAccount = account
                break
        self.do_login()

    def un_init(self):
        self.stop(True)

    def main_loop(self):
        while True:
            cmd = input("请输入命令：退出(quit)、启动(start)、暂停(stop)、重新登录(login)")
            if cmd == "quit":
                break
            elif cmd == "start":
                self.start()
            elif cmd == "stop":
                self.stop(True)
            elif cmd == "login":
                self.start_re_login()

    def init_completed(self):
        self.start()

    def start(self):
        self.stop()
        self.m_bServerRunning = True
        self.m_objTaskMgr.reset_running_time()
        self.m_threadTask = Thread(target=self.task_run)
        self.m_threadTask.setDaemon(True)
        self.m_threadTask.start()

    def stop(self, is_user_operate=False):
        self.m_bServerRunning = False
        if self.m_threadTask is not None:
            try:
                self.m_threadTask.join(5)
                self.m_threadTask = None
            except Exception as ex:
                self.logger.error("终止任务失败：{}".format(str(ex)))
        if is_user_operate:
            self.m_bIsReLogin = False
        else:
            self.m_bIsReLogin = True

    def notify_state(self, status):
        self.m_objAccount.m_eAccountStatus = status

    def refresh_player(self):
        pass

    def notify_single_task(self, task_name):
        if self.m_objTaskMgr is not None:
            self.m_objTaskMgr.run_single_task(task_name)

    def start_re_login_timer(self):
        self.start_re_login_timer_impl(1800)

    def start_re_login_timer_impl(self, wait_seconds):
        if wait_seconds == 0:
            self.start_re_login()
        elif self.m_timerReLogin is None:
            self.logger.info("将在{}后开始重新登录".format("{}分钟".format(wait_seconds / 60) if wait_seconds >= 60 else "{}秒".format(wait_seconds)))
            self.start_re_login_thread(wait_seconds)

    def start_re_login(self):
        try:
            self.m_bIsReLogin = True
            self.stop_re_login_thread()
            self.do_login()
        except Exception as ex:
            self.logger.error("重新登录定时器异常：{}".format(str(ex)))

    def start_re_login_thread(self, wait_seconds):
        self.stop_re_login_thread()
        self.m_timerReLogin = Timer(wait_seconds, self.start_re_login)
        self.m_timerReLogin.start()

    def stop_re_login_thread(self):
        if self.m_timerReLogin is not None:
            self.m_timerReLogin.cancel()
            self.m_timerReLogin = None

    def task_run(self):
        while self.m_bServerRunning:
            if self.m_objTaskMgr is not None:
                self.m_objTaskMgr.run_all_task()
            time.sleep(0.1)

    def do_login(self):
        cookies = requests.cookies.RequestsCookieJar()
        login_mgr = LoginMgr()
        login_result = login_mgr.login(self.m_objAccount, cookies)
        if login_result is None:
            self.logger.info("登录失败，请重试")
            self.start_re_login_timer_impl(30)
        elif login_result.m_eLoginStatus == LoginStatus.Success:
            self.init_game(login_result)
        else:
            self.logger.info(login_result.get_login_status_desc())
            self.start_re_login_timer_impl(30)

    def init_game(self, login_result):
        self.m_objAccount.m_eAccountStatus = AccountStatus.NotStart
        self.m_objAccount.m_distCookies = login_result.m_dictCookies
        self.m_objAccount.m_szGameUrl = login_result.m_szGameUrl
        self.m_objAccount.m_szJSessionId = login_result.m_szJSessionId
        self.init_session()

    def init_session(self):
        self.m_objUser = User()
        self.m_objServiceFactory = ServiceFactory()
        self.m_objProtocolMgr = ProtocolMgr(self.m_objUser, self.m_objAccount.m_szGameUrl, self.m_objAccount.m_szJSessionId, self.m_objServiceFactory, self)
        self.m_objTaskMgr = TaskMgr()
        self.m_objServiceFactory.get_misc_mgr().get_server_time()
        if self.m_objServiceFactory.get_misc_mgr().get_player_info_by_user_id(self.m_objAccount.m_szRoleName):
            self.init_logging()
            self.build_services()
            self.m_objTaskMgr.set_variables(self.m_objServiceFactory, self.m_objProtocolMgr, self.m_objUser, self)
            self.m_objTaskMgr.init()
            self.init_completed()

    def init_logging(self):
        partner = ServerTypeString.get_desc(self.m_objAccount.m_eServerType).decode("utf-8").encode("gbk")
        username = self.m_objUser.m_szUserName.decode("utf-8").encode("gbk")
        path = "logs/{}_{}_{}".format(partner, self.m_objAccount.m_nServerId, username)
        if not os.path.exists(path):
            os.makedirs(path)
        file_handler = TimedRotatingFileHandler("{}/astd.log".format(path), when="D", interval=1)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_handler)

    def build_services(self):
        self.m_objTaskMgr.add_task(CommonTask())
        self.m_objTaskMgr.add_task(FeteTask())
        self.m_objTaskMgr.add_task(ImposeTask())
        self.m_objTaskMgr.add_task(TicketTask())
        self.m_objTaskMgr.add_task(SupperMarketTask())
