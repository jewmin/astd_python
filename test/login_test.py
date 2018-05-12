# -*- coding: utf-8 -*-
import requests

from model.account import Account
from model.enum.server_type import ServerType
from manager.login_mgr import LoginMgr
import logging
from model.enum.account_status import AccountStatus
from model.user import User
from manager.protocol_mgr import ProtocolMgr
from manager.service_factory import ServiceFactory
from model.enum.login_status import LoginStatus
from manager.task_mgr import TaskMgr
from logic.common_task import CommonTask


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(filename)s [%(levelname)s] %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename="astd.log")
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    account = Account()
    account.m_szUserName = "jewmin"
    account.m_szPassword = "1986czm"
    account.m_eServerType = ServerType.YaoWan
    account.m_nServerId = 211
    account.m_szRoleName = "杯具"

    cookies = requests.cookies.RequestsCookieJar()
    login_mgr = LoginMgr()
    login_result = login_mgr.login(account, cookies)
    if login_result.m_eLoginStatus == LoginStatus.Success:
        init_game(account, login_result)
    else:
        logging.getLogger().info("重新登录失败")


def init_game(account, login_result):
    account.m_eAccountStatus = AccountStatus.NotStart
    account.m_distCookies = login_result.m_dictCookies
    account.m_szGameUrl = login_result.m_szGameUrl
    account.m_szJSessionId = login_result.m_szJSessionId
    init_session(account)


def init_session(account):
    user = User()
    factory = ServiceFactory()
    protocol_mgr = ProtocolMgr(user, account.m_szGameUrl, account.m_szJSessionId, factory)
    task_mgr = TaskMgr()
    factory.get_misc_mgr().get_server_time()
    if factory.get_misc_mgr().get_player_info_by_user_id(account.m_szRoleName):
        build_services(task_mgr)
        task_mgr.set_variables(factory, protocol_mgr, user)
        task_mgr.init()
        init_completed(task_mgr)


def build_services(task_mgr):
    task_mgr.add_task(CommonTask())


def init_completed(task_mgr):
    task_mgr.reset_running_time()
    task_mgr.run_all_task()


if __name__ == "__main__":
    main()
