"""
project: apiAutoTestWeb
file: project.py
author: zy7y
date: 2021/4/18
desc: 项目路由
"""
from fastapi import APIRouter
from tortoise.transactions import in_transaction

import core
from db import models

projects = APIRouter(tags=['项目相关'])


@projects.post("/project", name="创建项目")
async def create(project: models.ProjectIn_Pydantic):
    """
    :param project: name 字段唯一

    :return:
    """
    try:
        project_obj = await models.Project.create(**project.dict(exclude_unset=True))
        # from_tortoise_orm 从 数据表中序列化， 针对 模型类对象
        return core.Success(data=await models.Project_Pydantic.from_tortoise_orm(project_obj))
    except Exception as e:
        return core.Fail(message="项目已存在.")


@projects.delete("/project/{p_id}", name="删除项目")
async def delete(p_id: int):
    project_obj = await models.Project.filter(id=p_id).delete()
    if project_obj:
        return core.Success()
    return core.Fail(message="项目不存在.")


# https://tortoise-orm.readthedocs.io/en/latest/CHANGELOG.html?highlight=from_queryset_single#id27
@projects.get("/project", name="获取所有项目")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Project_Pydantic.from_queryset(models.Project.all().order_by('-created_at').offset(skip).limit(limit))
    # await models.Project.all().count()
    return core.Success(data={"total": await models.Project.all().count(), "items": data})


@projects.get("/project/{p_id}", name="获取项目详细")
async def select(p_id: int):
    data = await models.Project_Pydantic.from_queryset_single(models.Project.get(id=p_id))
    return core.Success(data=data)


@projects.put("/project/{p_id}", name="编辑项目")
async def update(p_id: int, project: models.ProjectIn_Pydantic):
    await models.Project.filter(id=p_id).update(**project.dict(exclude_unset=True))
    return core.Success(data=await models.Project_Pydantic.from_queryset_single(models.Project.get(id=p_id)))


@projects.get("/project/{p_id}/cases", name="获取项目下所有用例")
async def get_cases(p_id: int):
    sql = f"select 'case'.id, 'case'.name, 'case'.interface_id from 'case', interface WHERE  interface.id = 'case'.interface_id AND interface.project_id ={p_id};"
    async with in_transaction("default") as conn:
        data = await conn.execute_query_dict(sql)
    return core.Success(data={"total": len(data), "items": data})


@projects.get("/projects", name="获取所有项目不分页")
async def get_projects():
    data = await models.Project_Pydantic.from_queryset(models.Project.all())
    return core.Success(data={"total": len(data), "items": data})
