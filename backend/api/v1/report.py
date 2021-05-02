#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@report: apiAutoTestFastApi
@File  :report.py
@Author:zy7y
@Date  :2021/4/29 18:53
@Desc  :
"""
from fastapi import APIRouter

import core
from db import models

reports = APIRouter(tags=["报告相关"])


@reports.delete("/report/{r_id}", name="删除报告")
async def delete(r_id: int):
    report_obj = await models.Report.filter(id=r_id).delete()
    if report_obj:
        return core.Success()
    return core.Fail(message="报告不存在.")


# https://tortoise-orm.readthedocs.io/en/latest/CHANGELOG.html?highlight=from_queryset_single#id27
@reports.get("/report", name="获取所有报告")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Report_Pydantic.from_queryset(models.Report.all().order_by('-created_at').offset(skip).limit(limit))
    # await models.report.all().count()
    return core.Success(data={"total": await models.Report.all().count(), "items": data})


@reports.get("/report/{r_id}", name="获取报告详细")
async def select(r_id: int):
    data = await models.Report_Pydantic.from_queryset_single(models.Report.get(id=r_id))
    return core.Success(data=data)
