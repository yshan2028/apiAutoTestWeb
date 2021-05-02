#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: apiAutoTestFastAPI
@File  :case.py
@Author:zy7y
@Date  :2021/4/21 13:06
@Desc  :
"""

from fastapi import APIRouter

import core
from db import models

cases = APIRouter(tags=["用例相关"])


@cases.post("/case", name="新增用例")
async def create(case: models.CaseIn_Pydantic):
    case_obj = await models.Case.create(**case.dict(exclude_unset=True))
    return core.Success(data=await models.Case_Pydantic.from_tortoise_orm(case_obj))


@cases.delete("/case/{c_id}", name="删除用例")
async def delete(c_id: int):
    case_obj = await models.Case.filter(id=c_id).delete()
    if case_obj:
        return core.Success()
    return core.Fail(message="用例不存在.")


@cases.get("/case", name="获取所有用例")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Case_Pydantic.from_queryset(models.Case.all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.Case.all().count(), "items": data})


@cases.get("/case/{c_id}", name="获取用例详细")
async def select(c_id: int):
    data = await models.Case_Pydantic.from_queryset_single(models.Case.get(id=c_id))
    return core.Success(data=data)


@cases.put("/case/{c_id}", name="编辑用例")
async def update(c_id: int, case: models.CaseIn_Pydantic):
    await models.Case.filter(id=c_id).update(**case.dict(exclude_unset=True))
    return core.Success(data=await models.Case_Pydantic.from_queryset_single(models.Case.get(id=c_id)))
