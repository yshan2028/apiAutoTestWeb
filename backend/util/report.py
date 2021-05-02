#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: apiAutoTestFastapi
@File  :report.py
@Author:zy7y
@Date  :2021/5/2 0:16
@Desc  : 单个用例响应模型
"""


def model(case: object, url: str, header: str):
    """单个用例响应模型"""
    return {
        "info": {
            "name": case.name,
            "interface": {
                "name": case.interface.name,
                "path": case.interface.path,
            }
        },
        "source": {
            "url": url + case.interface.path,
            "headers": header,
            "method": case.interface.method,
            "content_type": case.content_type,
            "data": case.body
        },
        "request": {
            "url": url + case.interface.path,
            "headers": header,
            "method": case.interface.method,
            "content_type": case.content_type,
            "data": "数据处理时发生异常,表达式值是否错误."
        },
        "response": {
            "data": "请求接口时出现异常,查看请求信息检查错误.",
            "time": None,
            "status": None
        },
        "extra": case.extra,
        "expect": case.expect
    }

