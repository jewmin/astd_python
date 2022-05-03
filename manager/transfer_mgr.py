# -*- coding: utf-8 -*-
# http管理
import zlib
import asyncio
from logging import getLogger
from aiohttp import ClientSession, ClientTimeout, ClientResponse
from requests.cookies import RequestsCookieJar


class TransferMgr:

    @staticmethod
    async def result(response:ClientResponse) -> str:
        if response is None or response.status_code == 0:
            return "code:-1"
        elif response.status_code != 200 and response.status_code != 304:
            return f"code:{response.status_code}"
        else:
            content = await response.text(encoding="utf-8")
            if response.headers["content-type"] == "application/x-gzip-compressed":
                content = zlib.decompress(content)
                start = content.index(b'<?xml')
                content = content[start:]
            content = content.decode()
            index = content.find("<results>")
            if index < 0:
                return ""
            else:
                return content[index:]

    @staticmethod
    async def get(url:str, cookies:RequestsCookieJar) -> str:
        response = await TransferMgr.get_pure(url, cookies)
        return await TransferMgr.result(response)

    @staticmethod
    async def post(url:str, data:dict, cookies:RequestsCookieJar) -> str:
        response = await TransferMgr.post_pure(url, data, cookies)
        return await TransferMgr.result(response)

    @staticmethod
    async def get_pure(url:str, cookies:RequestsCookieJar, headers:dict=None, allow_redirects:bool=False, ssl:bool=False) -> ClientResponse:
        try:
            async with ClientSession(loop=asyncio.get_event_loop(), timeout=ClientTimeout(total=5)) as session:
                async with session.get(url, cookies=cookies, headers=headers, allow_redirects=allow_redirects, ssl=ssl) as response:
                    cookies.update(response.cookies)
                    return response
        except Exception as ex:
            getLogger("TransferMgr").error("GET请求失败", exc_info=True)

    @staticmethod
    async def post_pure(url:str, data:dict, cookies:RequestsCookieJar, headers:dict=None, allow_redirects:bool=False, ssl:bool=False) -> ClientResponse:
        try:
            async with ClientSession(loop=asyncio.get_event_loop(), timeout=ClientTimeout(total=5)) as session:
                async with session.post(url, data=data, cookies=cookies, headers=headers, allow_redirects=allow_redirects, ssl=ssl) as response:
                    cookies.update(response.cookies)
                    return response
        except Exception as ex:
            getLogger("TransferMgr").error("POST请求失败", exc_info=True)
