# -*- coding: utf-8 -*-
# 协议管理
from logging import getLogger
from urlparse import urlparse
import requests
from manager.transfer_mgr import TransferMgr
from model.server_result import ServerResult


class ProtocolMgr(object):
    def __init__(self, user, game_url, j_session_id, service_factory):
        super(ProtocolMgr, self).__init__()
        self.logger = getLogger(self.__class__.__name__)
        self.m_objUser = user
        self.m_objServiceFactory = service_factory
        self.m_objServiceFactory.set_protocol_mgr(self)

        url = urlparse(game_url)
        self.m_szGameUrl = "{}://{}".format(url.scheme, url.netloc)
        self.m_objJar = requests.cookies.RequestsCookieJar()
        self.m_objJar.set("JSESSIONID", j_session_id, domain=url.hostname, path="/root")

    def get_user(self):
        return self.m_objUser

    def get_xml(self, url, desc):
        self.logger.info(desc)
        server_result = self.get(url)
        self.handle_result(server_result)
        return server_result

    def post_xml(self, url, data, desc):
        self.logger.info(desc)
        server_result = self.post(url, data)
        self.handle_result(server_result)
        return server_result

    def handle_result(self, server_result):
        if server_result is not None:
            self.logger.debug(server_result.get_debug_info())
            if server_result.is_http_succeed():
                if server_result.m_bSucceed:
                    if "playerupdateinfo" in server_result.m_objResult:
                        self.m_objUser.update_player_info(server_result.m_objResult["playerupdateinfo"])
                    if "playerbattleinfo" in server_result.m_objResult:
                        self.m_objUser.update_player_battle_info(server_result.m_objResult["playerbattleinfo"])
                elif "连接已超时" in server_result.m_szError or "用户已在别处登陆" in server_result.m_szError:
                    raise Exception("需要重新登录")

    def get(self, url):
        real_url = "{}{}?{}".format(self.m_szGameUrl, url, self.m_objServiceFactory.get_time_mgr().get_timestamp())
        self.logger.debug("get url={}".format(real_url))
        try:
            return ServerResult(TransferMgr.get(real_url, self.m_objJar))
        except Exception as ex:
            self.logger.error(str(ex))

    def post(self, url, data):
        real_url = "{}{}?{}".format(self.m_szGameUrl, url, self.m_objServiceFactory.get_time_mgr().get_timestamp())
        self.logger.debug("post url={} data={}".format(real_url, data))
        try:
            return ServerResult(TransferMgr.post(real_url, data, self.m_objJar))
        except Exception as ex:
            self.logger.error(str(ex))
