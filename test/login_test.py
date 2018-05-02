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
    account.m_szUserName = "jewminchan"
    account.m_szPassword = "1986czm"
    account.m_eServerType = ServerType.YaoWan
    account.m_nServerId = 265
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
    factory.get_misc_mgr().get_server_time()
    # factory.get_misc_mgr().get_player_info_by_user_id(account.m_szRoleName)
    # print(factory.get_misc_mgr().immediate())
    # print(factory.get_misc_mgr().an_hour_later())
    # print(factory.get_misc_mgr().next_half_hour())
    # print(factory.get_misc_mgr().next_hour())
    # print(factory.get_misc_mgr().next_dinner())
    # print(factory.get_misc_mgr().next_day())
    # print(factory.get_misc_mgr().next_day(8))
    result = protocol.get_xml("/root/server!getPlayerInfoByUserId.action", "获取玩家信息")
    # data = {"playerId": result.m_objResult["player"][1]["playerid"], "code": result.m_objResult["code"]}
    # result = protocol.post_xml("/root/server!chooseRole.action", data, "选择玩家角色")
    # result = protocol.get_xml("/root/server!getPlayerInfoByUserId.action", "获取玩家信息")
    result = protocol.get_xml("/root/mainCity.action", "获取主城信息")
    result = protocol.get_xml("/root/server!getExtraInfo.action", "获取玩家额外信息")
    result = protocol.get_xml("/root/server!getPlayerExtraInfo2.action", "获取玩家额外信息")
    # print(result)


if __name__ == "__main__":
    main()
