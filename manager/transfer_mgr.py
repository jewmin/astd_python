# -*- coding: utf-8 -*-
# http管理
from logging import getLogger
import requests
import zlib


class TransferMgr(object):
    @staticmethod
    def response(result):
        if result is None or result.status_code == 0:
            return "code:-1"
        elif result.status_code != 200 and result.status_code != 304:
            return "code:{}".format(result.status_code)
        else:
            if result.headers["content-type"] == "application/x-gzip-compressed":
                content = zlib.decompress(result.content)
            else:
                content = result.content
            index = content.find("<results>")
            if index < 0:
                return ""
            else:
                return content[index:]

    @staticmethod
    def get(url, cookies):
        result = TransferMgr.get_pure(url, cookies)
        return TransferMgr.response(result)

    @staticmethod
    def post(url, data, cookies):
        result = TransferMgr.post_pure(url, data, cookies)
        return TransferMgr.response(result)

    @staticmethod
    def get_pure(url, cookies, headers=None):
        try:
            session = requests.session()
            response = session.get(url=url, cookies=cookies, headers=headers, allow_redirects=False)
            cookies.update(session.cookies)
            return response
        except Exception as ex:
            getLogger("TransferMgr").error(str(ex))

    @staticmethod
    def post_pure(url, data, cookies, headers=None):
        try:
            session = requests.session()
            response = session.post(url=url, data=data, cookies=cookies, headers=headers, allow_redirects=False)
            cookies.update(session.cookies)
            return response
        except Exception as ex:
            getLogger("TransferMgr").error(str(ex))
