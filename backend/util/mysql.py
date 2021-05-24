#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: backend
@File  :mysql.py
@Author:zy7y
@Date  :2021/5/23 23:42
@Desc  : 数据库连接
"""

import aiomysql


async def connect(setting: dict):
    """
    连接mysql 数据库连接
    Args:
        setting:
        参考schemas MysqlSettings
    Returns:
        连接对象 or 异常信息
    """
    try:
        conn = await aiomysql.connect(**setting)
        return conn
    except Exception as e:
        return e.__str__()
