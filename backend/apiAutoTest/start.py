#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: backend
@File  :start.py
@Author:zy7y
@Date  :2021/5/29 23:47
@Desc  :启动方法
"""

from apiAutoTest import report
from apiAutoTest.common import Common
from apiAutoTest.handle import Handle
from apiAutoTest.mysql import Mysql
from apiAutoTest.request import ApiAutoTestWebClient


class Start:

    @classmethod
    async def run(cls, test_suite: object):
        """
        测试运行方法
        :param test_suite: 任务对象
        :return:
        """
        # 用例集信息
        suite_info = []

        suite_data = {
            "pass": 0,
            "fail": 0,
            "expect": 0,
            "project": test_suite.env.project.name
        }

        # 初始化
        handle = Handle(test_suite.env.base_header, test_suite.env.base_url)
        db = test_suite.env.db_settings

        async def basic(db_bool: Mysql = None):
            """
            公共的测试方法
            :param db_bool: 数据库对象
            :return:
            """
            for case in test_suite.cases:
                try:
                    # 0. 日志初始化
                    case_info = report.model(
                        case, test_suite.env.base_url, handle.header(
                            case.case_header))

                    case_info["info"] = {
                        "name": case.name,
                        "interface": {
                            "name": case.interface.name,
                            "path": case.interface.path,
                        }
                    }
                    case_info["source"] = {
                        "url": test_suite.env.base_url + case.interface.path,
                        "headers": case.case_header,
                        "method": case.interface.method,
                        "content_type": case.content_type,
                        "data": case.body
                    }
                    # 1. 处理header
                    headers = handle.header(case.case_header)
                    # 2. 处理url
                    path = handle.path(case.interface.path)
                    # 3. 拿到method
                    method = case.interface.method
                    # 4. 获取入参类型
                    content_type = case.content_type
                    # 5. 处理请求数据
                    data = handle.body(case.body)
                    # 6. 发起请求
                    info = await ApiAutoTestWebClient.request(headers, path, method, content_type, data)
                    # 6.1 日志合并
                    case_info.update(info)
                    # 7. 获取到响应json内容
                    response = Common.extra_jsonpath(info, '$.response.data')
                    # 8. 提取参数
                    extra = handle.extra(case.extra, response)
                    # 8.1 日志合并
                    case_info["extra"] = extra
                    # 9. 后置sql
                    sql_info = handle.sql(case.backend_sql, db_bool)
                    # 9.1 日志合并
                    case_info["backend_sql"] = sql_info
                    # 10. 断言
                    result_info, result = handle.equal(case.expect, response)
                    case_info["expect"] = result_info
                    if result:
                        case_info["result"] = "正常"
                        suite_data["pass"] += 1
                    else:
                        case_info["result"] = "失败"
                        suite_data["fail"] += 1
                except Exception as e:
                    print(e)
                    case_info["result"] = "异常"
                    suite_data["expect"] += 1
                    case_info["error_code"] = str(e)

            suite_info.append(case_info)

        if db is not None:
            # todo 应避免不可靠的数据库连接使用sql
            mysql = Mysql()
            await mysql.connect(db)
            await basic(mysql)
            mysql.close()
        else:
            await basic()

        suite_data["suite_info"] = suite_info

        return suite_data
