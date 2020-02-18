# -*- coding: utf-8 -*-
# 返回结果
from logging import getLogger
from model.xml_parse import XmlParse


class ServerResult(object):
    def __init__(self, url, result, index):
        super(ServerResult, self).__init__()
        self.logger = getLogger(index)
        self.m_nHttpCode = 0
        self.m_bSucceed = False
        self.m_szError = ""
        self.m_objResult = None
        self.m_szXml = ""
        self.m_szUrl = url
        if result is not None and result != "":
            if result.startswith("code:"):
                self.m_nHttpCode = int(result.replace("code:", ""))
            elif result.startswith("E"):
                self.m_nHttpCode = 200
                self.m_szError = result
            else:
                self.m_nHttpCode = 200
                try:
                    # 过滤掉非法字符&
                    result = result.replace("&", "")
                    self.m_objResult = XmlParse().parse(result)["results"]
                    if self.m_objResult.get("state", "0") == "1":
                        self.m_bSucceed = True
                        self.m_szXml = result
                    else:
                        if "message" in self.m_objResult:
                            self.m_szError = self.m_objResult["message"]
                        elif "exception" in self.m_objResult:
                            self.m_szError = self.m_objResult["exception"]
                        if self.m_szError == "":
                            self.m_szError = result
                except Exception as ex:
                    self.m_szError = str(ex)
                    self.logger.error("解析结果失败：{}".format(self.m_szError))

    def is_http_succeed(self):
        return self.m_nHttpCode == 200

    def get_http_error_info(self):
        if self.m_nHttpCode == -1:
            return "断网"
        elif self.m_nHttpCode == 404:
            return "404 未找到网页"
        elif self.m_nHttpCode == 500:
            return "500 服务器错误"
        else:
            return "错误码: {}".format(self.m_nHttpCode)

    def get_debug_info(self):
        if not self.is_http_succeed():
            return self.get_http_error_info()
        elif not self.m_bSucceed:
            return self.m_szError
        else:
            return self.m_szXml

    def get_url(self):
        return self.m_szUrl
