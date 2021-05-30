#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: backend
@File  :request.py
@Author:zy7y
@Date  :2021/5/25 23:20
@Desc  :
"""
import time

import aiohttp
from aiohttp import ClientResponse, FormData


class ApiAutoTestWebClient:

    @classmethod
    async def aiohttp_client(cls, method: str, url: str, **kwargs) -> ClientResponse:
        """
        发起请求
        method: str,
        str_or_url: StrOrURL,
        *,
        params: Optional[Mapping[str, str]] = None,
        data: Any = None,
        json: Any = None,
        cookies: Optional[LooseCookies] = None,
        headers: Optional[LooseHeaders] = None,
        skip_auto_headers: Optional[Iterable[str]] = None,
        auth: Optional[BasicAuth] = None,
        allow_redirects: bool = True,
        max_redirects: int = 10,
        compress: Optional[str] = None,
        chunked: Optional[bool] = None,
        expect100: bool = False,
        raise_for_status: Optional[bool] = None,
        read_until_eof: bool = True,
        proxy: Optional[StrOrURL] = None,
        proxy_auth: Optional[BasicAuth] = None,
        timeout: Union[ClientTimeout, object] = sentinel,
        verify_ssl: Optional[bool] = None,
        fingerprint: Optional[bytes] = None,
        ssl_context: Optional[SSLContext] = None,
        ssl: Optional[Union[SSLContext, bool, Fingerprint]] = None,
        proxy_headers: Optional[LooseHeaders] = None,
        trace_request_ctx: Optional[SimpleNamespace] = None,
        read_bufsize: Optional[int] = None,
        :return:
        """
        async with aiohttp.ClientSession() as session:
            start = time.time()
            response = await session.request(method, url, **kwargs)
            end = time.time()
            try:
                # https://stackoverflow.com/questions/48840378/python-attempt-to-decode-json-with-unexpected-mimetype
                resp_data = await response.json(content_type=None)
            except Exception as e:
                resp_data = {
                    "type": "error",
                    "form": "apiAutoTestWeb",
                    "msg": str(e)}
            return {
                "request": {
                    "url": response.request_info.url.__str__(),
                    "method": response.request_info.method,
                    "headers": dict(response.request_info.headers),
                    "real_url": response.request_info.real_url.__str__()
                },
                "response": {
                    "data": resp_data,
                    "time": int((end - start) * 1000),
                    "status": response.status
                }
            }

    @classmethod
    def upload(cls, files: dict):
        """
        上传文件：https://docs.aiohttp.org/en/stable/client_quickstart.html
        :param files:
                {
            "file_var": "file",   # 接受文件的参数 必须有
            "file_path": "C:/Users/zy7y/Desktop/v2-45497fca1dcca976eb00fc475eefdc40_720w.jpg" 必须有
            "filename": "上传服务器之后保存的文件名",
            "content_type": "设置头部信息"
        }
        :return:
        """
        body = FormData()  # 指定表单的上传文件
        body.add_field(files.get("file_var", "file"),
                       open(files.get("file_path"), 'rb'),
                       filename=files.get("filename", None),
                       content_type=files.get("content_type", None))
        return body

    @classmethod
    async def request(
            cls,
            headers: dict,
            url: str,
            method: str,
            content_type: str,
            data: dict = None,
            **kwargs) -> dict:
        """
        请求处理，根据content_type区分入参关键字
        :param headers: 请求头
        :param url: 请求地址
        :param method: 请求方法
        :param content_type: 入参类型
        :param data: 请求数据
        :param kwargs: 关键字参数，接受一个字典可扩展
        :return: {"data": 响应内容(json), "time": 响应时间(ms), "status": 状态码}
        """

        content_type = content_type.upper()
        if content_type == "JSON":
            return await cls.aiohttp_client(headers=headers, url=url, method=method, json=data, **kwargs)
        elif content_type == "PARAMS":
            return await cls.aiohttp_client(headers=headers, url=url, method=method, params=data, **kwargs)
        elif content_type == "DATA":

            return await cls.aiohttp_client(headers=headers, url=url, method=method, data=data, **kwargs)
        elif content_type == "FILES":
            return await cls.aiohttp_client(headers=headers, url=url, method=method, data=cls.upload(data), **kwargs)


if __name__ == '__main__':

    import asyncio

    # data = {"params": {"page": 1}}
    # result = asyncio.run(HTTPClient.aiohttp_client(
    #     "get", "http://49.232.203.244:8000/message", params={"page": 1}))
    # res, res_time = result
    # print(res.status, res_time)
    # 上传文件
    data = {
        "file_var": "file",  # 接口中接受文件参数的 名称
        "file_path": "C:/Users/zy7y/Desktop/v2-45497fca1dcca976eb00fc475eefdc40_720w.jpg",  # 必要 的 本地文件地址
        "filename": "花花工资",     # 可以指定上传文件之后服务器保存的名称
        "content_type": None    # 可以指定 上传文件 的类型
    }
    # print(asyncio.run(HTTPClient.request(
    #     {}, "http://127.0.0.1:8888/upload_file/", "post", "files", data)))

    print(asyncio.run(ApiAutoTestWebClient.request(
        {}, "http://49.232.203.244:8001/v1/post", "get", "params", {"page":1})))

    url = "http://www.ysqorz.top:8888/api/private/v1/login"
    print(asyncio.run(ApiAutoTestWebClient.request(
        {}, url, "post", "data", {"username": "admin", "password": "123456"})))
