#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: apiAutoTestFastAPI
@File  :enum_filed.py
@Author:zy7y
@Date  :2021/4/22 21:40
@Desc  : 枚举类的字段
"""
from enum import Enum


class Methods(str, Enum):
    """请求方法类型"""
    POST = 'post'
    DELETE = 'delete'
    GET = 'get'
    PUT = 'put'


# https://www.runoob.com/http/http-content-type.html
class ContentType(str, Enum):
    """请求参数类型"""
    PARAMS = 'params'
    DATA = 'data'
    JSON = 'json'


class Standard(str, Enum):
    """接口规范"""
    RESTFUL = 'restful'
    GRAPHQL = 'graphql'
