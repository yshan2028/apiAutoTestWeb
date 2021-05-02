#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: FastAPI
@File  :apiAutoTest.py
@Author:zy7y
@Date  :2021/4/26 22:24
@Desc  : 实现apiAutoTest 核心部分
"""
import re
import json
import time

import aiohttp
from jsonpath import jsonpath
from string import Template

from util import report
from .extend import *
import traceback


class ApiAutoTest:

    @classmethod
    async def exec_func(cls, func: str):
        """
        执行自定义扩展方法
        Args:
            func: 方法名() / 方法名(参数1, 参数2)

        Returns:
            result: 方法返回值
        """
        loc = locals()
        exec(f"result = {func}")
        return str(loc['result'])

    @classmethod
    async def request(cls, method: str, url: str, content_type: str, data: dict, header: dict, info: dict) -> dict:
        """
        请求方法， aiohttp官方不推荐一次使用一个session ，不推荐使用request对象
        Args:
            method: 请求方法
            url: 最终请求地址
            content_type: 请求参数格式
            data: 请求参数
            header: 请求头
            info: 记录数据

        Returns:
            resp.json(): 接口响应
        """
        info["request"] = {
            "url": url,
            "headers": header,
            "method": method,
            "content_type": content_type,
            "data": data
        }

        # aiohttp 建议使用一个session 对象, 如下方法调用一次都会创建一次，删除一次
        async with aiohttp.ClientSession() as session:
            if content_type == "json":
                start = time.time()
                resp = await session.request(method, url, json=data, headers=header)
                end = time.time()
            elif content_type == "data":
                start = time.time()
                resp = await session.request(method, url, data=data, headers=header)
                end = time.time()
            else:
                start = time.time()
                resp = await session.request(method, url, params=data, headers=header)
                end = time.time()

            res = await resp.json()
            info["response"] = {
                "data": await resp.json(),
                "time": int((end - start) * 1000),
                "status": resp.status
            }

            return res

    @classmethod
    async def template_var(cls, var: str, data_pool: dict, is_path: bool = False) -> str:
        """
        替换依赖变量数据，以及自定义扩展方法
        Args:
            var: 待替换的字符串
            data_pool: 依赖参数变量池子
            is_path: 如果是path 就不用json化
        Returns:
            var: 替换之后的字符串内容
        """
        if var is None:
            return {}
        var = Template(var).safe_substitute(data_pool)
        for func in re.findall('\\${(.*?)}', var):
            try:
                var = var.replace('${%s}' % func, await cls.exec_func(func))
            except Exception as e:
                continue
        if is_path:
            return var
        try:
            var = json.loads(var)
        except Exception as e:
            # 处理如果有None
            var = json.dumps(eval(var))
        return var

    @classmethod
    async def get_operation_name(cls, query: str):
        try:
            # 有参数的query语句
            result = re.findall(' (.*?)\\(', query)[0]
        except IndexError:
            # 无参数的query语句
            result = re.findall(' (.*?){', query)[0]
        return result

    @classmethod
    async def handle_case(cls, case: dict, data_pool: dict, base_header: str):
        """
        处理单一case
        Args:
            case: 一个用例对象
            data_pool: 变量储存池
            base_header: 待处理header

        Returns:

        """
        method = case.interface.method
        content_type = case.content_type
        # 处理Path, 替换参数依赖变量
        path = await cls.template_var(case.interface.path, data_pool, is_path=True)
        body = await cls.template_var(case.body, data_pool)
        extra = await cls.template_var(case.extra, data_pool)
        expect = await cls.template_var(case.expect, data_pool)
        header = await cls.template_var(base_header, data_pool)

        # graphql 规范组装 请求数据
        if case.interface.standard == 'graphql':
            body = {"operationName": await cls.get_operation_name(case.query), "query": case.query, "variables": body}

        return method, content_type, path, body, extra, expect, header

    @classmethod
    async def extra_var(cls, extra_json: dict, data_pool: dict, resp: dict):
        """
        使用jsonpath语法进行参数提取，key 作为参数名，value作为jsonpath提取语法
        Args:
            extra_json: 提取参数的json内容 {"变量名": "jsonpath语法"}
            data_pool: 用例集参数池，存放提取的参数键值对
            resp: 提取源，接口响应

        Returns:

        """
        for k, v in extra_json.items():
            data_pool[k] = jsonpath(resp, v)[0]

    @classmethod
    async def equal(cls, expect_json: dict, resp: dict, info: dict) -> str:
        """
        断言，{"实际结果": "预期结果"}，支持多个断言，实际结果建议使用jsonpath语法从接口响应获取, 预期结果可以使用${变量}、${方法}
        Args:
            expect_json: 预期结果的json内容, {"实际结果": "预期结果"}
            resp: 提取源, 接口响应， 主要用于实际结果获取
            info: 记录信息
        Returns:

        """
        info["expect"] = []
        result = "异常"
        for k, v in expect_json.items():
            info["expect"].append(
                {f"{k} ? {v}": f'{jsonpath(resp, k)[0]} == {v}'})
            if jsonpath(resp, k)[0] == v:
                result = "正常"
            else:
                result = "失败"
        info["result"] = result
        return result

    @classmethod
    async def test(cls, test_suite: object):
        """
        接口测试方法, 传入一个用例集[用例1， 用例2]
        Args:
            test_suite: 用例集，是个列表

        Returns:

        """
        # 日志信息池
        test_suite_info = []
        test_suite_data = {
            "pass": 0,
            "fail": 0,
            "expect": 0,
            "project": test_suite.env.project.name
        }
        # 局部变量池，作用于 整个测试
        data_pool: dict = {}
        # 解析 base_url
        base_url = test_suite.env.base_url
        base_header = test_suite.env.base_header

        # 得到case 列表
        for case in test_suite.cases:
            info = report.model(case, base_url, base_header)
            try:
                method, content_type, path, body, extra, expect, header = await cls.handle_case(case, data_pool, base_header)
                # 请求接口
                res = await cls.request(method, base_url + path, content_type, body, header, info)
                # 提取参数
                await cls.extra_var(extra, data_pool, res)
                # 断言
                result = await cls.equal(expect, res, info)
                if result == "正常":
                    test_suite_data["pass"] += 1
                else:
                    test_suite_data["fail"] += 1

            except Exception as e:
                info["error_code"] = traceback.format_exc()
                info["result"] = "异常"
                test_suite_data["expect"] += 1
                continue
            finally:
                info.get("")
                info["pool"] = data_pool
                test_suite_info.append(info)
        test_suite_data["suite_info"] = test_suite_info
        return test_suite_data
