#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: backend
@File  :mysql.py
@Author:zy7y
@Date  :2021/5/23 23:42
@Desc  : 数据库连接
"""
from datetime import datetime
from typing import Union

import ujson
from aiomysql import connect, cursors


class Mysql:
    # https://aiomysql.readthedocs.io/en/latest/tutorial.html
    conn = None

    async def connect(self, setting: dict):
        try:
            self.conn = await connect(**setting, cursorclass=cursors.DictCursor)
        except Exception as e:
            print(e)

    async def exec_sql(self, sql: str):
        async with self.conn.cursor() as cur:
            await cur.execute(sql)
            result = await cur.fetchone()
            await self.conn.commit()
            return self.verify(result)

    def verify(self, result: dict) -> Union[dict, None]:
        """验证结果能否被json.dumps序列化"""
        # 尝试变成字符串，解决datetime 无法被json 序列化问题
        try:
            ujson.dumps(result)
        except TypeError:  # TypeError: Object of type datetime is not JSON serializable
            for k, v in result.items():
                if isinstance(v, datetime):
                    result[k] = str(v)
        return result

    def close(self):
        self.conn.close()
