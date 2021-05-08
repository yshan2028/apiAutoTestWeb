#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: apiAutoTestFastAPI
@File  :inteface.py
@Author:zy7y
@Date  :2021/4/21 13:06
@Desc  :
"""
from fastapi import APIRouter

import core
from db import models
from util.import_interface import ImportInterface

interfaces = APIRouter(tags=["接口相关"])


@interfaces.post("/interface", name="新增接口")
async def create(interface: models.InterfaceIn_Pydantic):
    try:
        interface_obj = await models.Interface.create(**interface.dict(exclude_unset=True))
        return core.Success(data=await models.Interface_Pydantic.from_tortoise_orm(interface_obj))
    except Exception as e:
        return core.Fail(message="创建失败.")


@interfaces.delete("/interface/{r_id}", name="删除接口")
async def delete(r_id: int):
    interface_obj = await models.Interface.filter(id=r_id).delete()
    if interface_obj:
        return core.Success()
    return core.Fail(message="接口不存在.")


@interfaces.get("/interface", name="获取所有接口")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Interface_Pydantic.from_queryset(models.Interface.all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.Interface.all().count(), "items": data})


@interfaces.get("/interface/{r_id}", name="获取接口详细")
async def select(r_id: int):
    data = await models.Interface_Pydantic.from_queryset_single(models.Interface.get(id=r_id))
    return core.Success(data=data)


@interfaces.put("/interface/{r_id}", name="编辑接口")
async def update(r_id: int, interface: models.InterfaceIn_Pydantic):
    await models.Interface.filter(id=r_id).update(**interface.dict(exclude_unset=True))
    return core.Success(data=await models.Interface_Pydantic.from_queryset_single(models.Interface.get(id=r_id)))


@interfaces.post("/interface/export", summary="接口导入,暂不支持用例生成")
async def export_interface(swagger: core.ExportInterface):
    """需要传入swagger 文档中的 openapi.json 地址 ：如 ~ http://49.232.203.244:8000/openapi.json """
    if swagger.url != "" and swagger.file is None:
        message = await ImportInterface.swagger(project_id=swagger.project_id, standard=swagger.standard, url=swagger.url)
        return core.Success(
            message=message) if '成功' in message else core.Fail(
            message=message)
    return core.Fail(message="导入失败,功能待开发.")
