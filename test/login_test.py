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
    account.m_szUserName = "cat000005"
    account.m_szPassword = "332211"
    account.m_eServerType = ServerType.YaoWan
    account.m_nServerId = 211
    account.m_szRoleName = ""

    cookies = requests.cookies.RequestsCookieJar()
    login_mgr = LoginMgr()
    login_result = login_mgr.login(account, cookies)
    init_game(account, login_result)


def init_game(account, login_result):
    account.m_eAccountStatus = AccountStatus.NotStart
    account.m_distCookies = login_result.m_dictCookies
    account.m_szGameUrl = login_result.m_szGameUrl
    account.m_szJSessionId = login_result.m_szJSessionId
    init_session(account)


def init_session(account):
    user = User()
    factory = ServiceFactory()
    protocol = ProtocolMgr(user, account.m_szGameUrl, account.m_szJSessionId, factory)
    result = protocol.get_xml("/root/server!getServerTime.action", "获取系统时间")
    print(result)
    result = protocol.get_xml("/root/server!getPlayerInfoByUserId.action", "获取玩家信息")
    print(result)


if __name__ == "__main__":
    main()
