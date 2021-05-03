#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: backend
@File  :import_interface.py
@Author:zy7y
@Date  :2021/5/3 21:46
@Desc  : 通过文档生成接口
"""

import aiohttp
from tortoise.transactions import in_transaction


class ImportInterface:

    @classmethod
    async def request(cls, url: str):
        async with aiohttp.ClientSession() as session:
            res = await session.get(url)
            return await res.json()

    @classmethod
    async def swagger(cls, project_id: int, url: str):
        try:
            async with in_transaction("default") as conn:
                if await conn.execute_query_dict(f"select id from project where id = {project_id}"):
                    num = 0
                    data = await cls.request(url)
                    for path, info in data["paths"].items():
                        # interface path -> k
                        for method, method_info in info.items():
                            # 插入数据库
                            # print(path, method, method_info["summary"], method_info.get("description", ""))
                            sql = f"""insert into interface (name, path, method, desc, standard, project_id) values
                        ("{method_info["summary"]}", "{path}","{method}", "{method_info.get("description", "")}", "restful", {project_id});"""
                            print(sql)
                            await conn.execute_query(sql)
                            num += 1
                    return f"成功导入{num}个接口."
        except Exception as e:
            return "导入失败,需要使用openapi.json文件URL"
        return "导入失败,项目不存在."
