#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: backend
@File  :hooks.py
@Author:zy7y
@Date  :2021/5/29 23:46
@Desc  :自定义扩展函数
"""
import time


def get_current_highest():
    """获取当前时间戳"""
    return int(time.time())
