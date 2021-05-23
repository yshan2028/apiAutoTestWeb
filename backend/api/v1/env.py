#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: apiAutoTestFastAPI
@File  :env.py
@Author:zy7y
@Date  :2021/4/19 21:18
@Desc  :
"""

from fastapi import APIRouter

import core
from db import models

envs = APIRouter(tags=["环境相关"])


@envs.post("/env", name="环境新增")
async def create(env: models.EnvIn_Pydantic):
    """
    环境新增数据库配置目前只提供mysql，需按照如下字典配置
    Args:
        env:

    Returns:

    """
    try:
        env_obj = await models.Env.create(**env.dict(exclude_unset=True))
        return core.Success(data=await models.Env_Pydantic.from_tortoise_orm(env_obj))
    except Exception as e:
        return core.Fail(message=f"创建失败.{e}")


@envs.delete("/env/{e_id}", name="环境删除")
async def delete(e_id: int):
    env_obj = await models.Env.filter(id=e_id).delete()
    if env_obj:
        return core.Success()
    return core.Fail(message="环境不存在.")


@envs.get("/env", name="查询所有环境")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Env_Pydantic.from_queryset(models.Env.all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.Env.all().count(), "items": data})


@envs.get("/env/{e_id}", name="环境详情")
async def select(e_id: int):
    try:
        data = await models.Env_Pydantic.from_queryset_single(models.Env.get(id=e_id))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看详情失败.{e}")


@envs.put("/env/{e_id}", name="环境编辑")
async def update(e_id: int, env: models.EnvIn_Pydantic):
    try:
        await models.Env.filter(id=e_id).update(**env.dict(exclude_unset=True))
        return core.Success(data=await models.Env_Pydantic.from_queryset_single(models.Env.get(id=e_id)))
    except Exception as e:
        return core.Fail(message=f"更新失败.{e}")
