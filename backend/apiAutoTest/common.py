#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: backend
@File  :common.py
@Author:zy7y
@Date  :2021/5/29 23:47
@Desc  : 公共方法
"""
import json
import re
from string import Template
from typing import Any

import ujson
from jsonpath import jsonpath

from .hooks import *


class Common:

    @staticmethod
    def exec_func(func: str) -> str:
        """
        执行字符串方法名
        :param func: 方法名
        :return:
        """
        loc = locals()
        exec(f"result = {func}")
        return str(loc['result'])

    @staticmethod
    def extra_jsonpath(obj: object, expr: str = '.') -> Any:
        """
        jsonpath 语法提取参数，如果提取不到返回表达式
        :param obj: 可被提取的对象，一般是json/dict
        :param expr: 提取表达式，默认提取所有内容
        :return:
        """
        result = jsonpath(obj, expr)
        if result:
            return result[0]
        return expr

    @staticmethod
    def replace_value(initial_value: str, data: dict) -> str:
        """
        将字符串中的${}语法替换，需要注意${}语法中不能再包含{}
        :param initial_value: 待替换值的字符串
        :param data: 当前已有的参数池
        :return:
        """
        if initial_value is None:
            return ''
        initial_value = Template(initial_value).safe_substitute(data)
        for func in re.findall('\\${(.*?)}', initial_value):
            try:
                initial_value = initial_value.replace('${%s}' % func, Common.exec_func(func))
            except Exception as e:
                print(e)
                continue
        return initial_value

    @staticmethod
    def str_json(data: str) -> dict:
        """
        字符串转json
        :param data: 待转成json的字符串
        :return:
        """
        try:
            return ujson.loads(data)  # ValueError: Expected object or value
        except ValueError:
            return {}


if __name__ == '__main__':
    result = Common.str_json("{'name': None}")
    print(result, type(result))

    result = json.dumps('[{"key":"value"},81,True]')
    print(result)
    result = ujson.loads('[{"key":"value"},81,null]')
    print(result)