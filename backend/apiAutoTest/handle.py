#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: backend
@File  :handle.py
@Author:zy7y
@Date  :2021/5/30 0:03
@Desc  : 处理case各部件类
"""
from typing import Union

from .mysql import Mysql
from .common import Common


class Handle:
    # 参数存放
    pool = {}

    def __init__(self, headers: dict = {}, base_url: str = ""):
        """
        初始化方法，传入环境header，基准地址
        :param headers: 基准header
        :param base_url: 基准地址
        """
        if headers is None:
            self.headers = {}
        else:
            self.headers = headers
        self.base_url = base_url

    def header(self, case_header: str) -> dict:
        """
        对请求header进行处理，最终合并成用例的header
        :param case_header: 用例header，其中可以使用${}、变量or方法
        :return: 覆盖之前的header内容，放到请求中
        """
        if case_header is None:
            case_header = ''
        case_header = Common.replace_value(case_header, self.pool)
        self.headers.update(Common.str_json(case_header))

    def path(self, path: str) -> str:
        """
        处理接口地址
        :param path: 接口地址
        :return:
        """
        return self.base_url + Common.replace_value(path, self.pool)

    def body(self, data: str) -> Union[dict, None]:
        """
        请求数据处理，
        :param data: 请求数据 -> str 的json
        :return:
        """
        if data != '':
            data = Common.replace_value(data, self.pool)
            return Common.str_json(data)

    def file(self):
        """
        文件处理
        :return:
        """
        pass

    def sql(self, sql_list: [str], db: Mysql = None) -> list:
        """
        执行sql语句, 传入一个列表
        :param db: 数据库连接对象
        :param sql_list: ["select * form user", "select * form role"]
        :return:
        """
        sql_info = []
        if sql_list is None:
            sql_list = []
        if len(sql_list) > 0 and db is not None:
            for s in sql_list:
                sql_str = Common.replace_value(s, self.pool)
                result = db.exec_sql()
                self.pool.update(result)
                sql_info.append({sql_str: result})
        return sql_info

    def extra(self, extra_dict: dict, resp: dict) -> dict:
        """
        提取参数，
        :param extra_dict: 提取参数字典内容，{"name": "$.data.name"}
        :param resp: 当前用例响应的json内容
        :return:
        """
        if extra_dict is None:
            extra_dict = {}
        for k, v in extra_dict.items():
            self.pool[k] = Common.extra_jsonpath(resp, v)
        return {"extra": self.pool}

    def equal(self, equal_dict: str, resp: dict) -> list:
        """
        断言相等,
        :param equal_dict: 断言字典, key 为实际结果 value 为 预期结果
        {"$.name": "柒意"} or {"name": "柒意"} or {"${name}": "柒意"} or {"$.name": "${name}"}
        :param resp: 当前用例的响应内容
        :return:
        """
        equal_info = []
        flag = True
        equal_dict = Common.str_json(equal_dict)
        for k, v in equal_dict.items():
            actual = Common.extra_jsonpath(resp, k)
            result = (actual == v)
            equal_info.append({
                f"断言内容: 预期{v} | 实际{k} => 最终实际结果, {actual}": result
            })
            if not result:
                flag = False

        return equal_info, flag

