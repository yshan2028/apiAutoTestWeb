#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: apiAutoTestFastApi
@File  :extend.py
@Author:zy7y
@Date  :2021/4/27 22:21
@Desc  : 自定义扩展方法
"""

import time


def sum_data(a, b):
    """"计算两数之和，在这个地方的脚本返回值都会被返回成str"""
    return a + b

def get_current_highest():
    """获取当前时间戳"""
    return int(time.time())