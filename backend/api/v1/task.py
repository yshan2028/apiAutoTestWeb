#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@task: apiAutoTestFastAPI
@File  :task.py
@Author:zy7y
@Date  :2021/4/24 16:41
@Desc  :
"""
import time

from tortoise.transactions import in_transaction

import core

from fastapi import APIRouter, BackgroundTasks
from db import models
from util import ApiAutoTest

from util import scheduler

tasks = APIRouter(tags=['任务相关'])


async def run_case(t_id: int):
    task_obj = await models.Task_Pydantic.from_queryset_single(models.Task.get(id=t_id))
    start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data = await ApiAutoTest.test(task_obj)
    end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    report_obj = await models.Report.create(name=task_obj.name, data=data, start=start, end=end, tasks_id=t_id)
    # return models.Report_Pydantic.from_tortoise_orm(report_obj)
    return report_obj.id


@tasks.post("/task", name="创建任务")
async def create(task: models.TaskInCase):
    """
    :param task: name 字段唯一

    :return:
    """
    # try:
    #     # 获取case对象，如果没有将抛出异常
    #     cases_obj = [await models.Case.get(id=case) for case in task.case_list]
    #     del task.case_list
    #
    #     # 定时任务, 事务        async with in_transaction():
    #
    #     if task.is_timer:
    #         trigger = scheduler.verif_cron(task.cron)
    #         if trigger:
    #             task_obj = await models.Task.create(**task.dict(exclude_unset=True))
    #             # 添加到多对多关系中
    #             await task_obj.cases.add(*cases_obj)
    #
    #             job = scheduler.new_job(str(task_obj.id), func=run_case, args=(
    #                 task_obj.id,), trigger=trigger)
    #             return core.Success(message=f"创建成功,下次运行的时间{job.next_run_time}")
    #         else:
    #             return core.Fail(message="corn表达式设置有误")
    #     else:
    #         task_obj = await models.Task.create(**task.dict(exclude_unset=True))
    #         # 添加到多对多关系中
    #         await task_obj.cases.add(*cases_obj)
    #     return core.Success(data=await models.Task_Pydantic.from_tortoise_orm(task_obj))
    # except Exception as e:
    #     print(e)
    #     return core.Fail(message="任务已存在.")
    try:
        # 事务来实现
        cases_obj = [await models.Case.get(id=case) for case in task.case_list]
        del task.case_list
        job_time = "待定"
        async with in_transaction():
            task_obj = await models.Task.create(**task.dict(exclude_unset=True))
            if task.is_timer:
                job = scheduler.new_job(str(task_obj.id), func=run_case, args=(
                    task_obj.id,), cron=task.cron)
                job_time = job.next_run_time
            await task_obj.cases.add(*cases_obj)
            return core.Success(message=f"创建成功,下次运行{job_time}")
    except Exception as e:
        return core.Fail(message=f"创建失败.{e}")


@tasks.delete("/task/{t_id}", name="删除任务")
async def delete(t_id: int):
    task_obj = await models.Task.filter(id=t_id).delete()
    if task_obj:
        try:
            scheduler.delete_job(str(t_id))
        except Exception as e:
            print(e)
        return core.Success()
    return core.Fail(message="任务不存在.")


# https://tortoise-orm.readthedocs.io/en/latest/CHANGELOG.html?highlight=from_queryset_single#id27
@tasks.get("/task", name="获取所有任务")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Task_Pydantic.from_queryset(models.Task.all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.Task.all().count(), "items": data})


@tasks.get("/task/{t_id}", name="获取任务详细")
async def select(t_id: int):
    data = await models.Task_Pydantic.from_queryset_single(models.Task.get(id=t_id))
    return core.Success(data=data)


@tasks.put("/task/{t_id}", name="编辑任务")
async def update(t_id: int, task: models.TaskInCase):
    try:
        task_obj = await models.Task.get(id=t_id)
        cases_obj = [await models.Case.get(id=case) for case in task.case_list]
        del task.case_list
        job_time = "待定"
        async with in_transaction():
            await models.Task.filter(id=t_id).update(**task.dict(exclude_unset=True))
            if task.is_timer:
                try:
                    job = scheduler.modify_job(
                        str(t_id), func=run_case, args=(
                            t_id,), cron=task.cron)
                except Exception as e:
                    print(e)
                    job = scheduler.new_job(
                        str(t_id), func=run_case, args=(
                            t_id,), cron=task.cron)
                job_time = job.next_run_time
            else:
                try:
                    scheduler.delete_job(str(task_obj.id))
                except Exception as e:
                    print(e)
            # 清除该对象与case的关系
            await task_obj.cases.clear()
            # 添加关系
            await task_obj.cases.add(*cases_obj)
            return core.Success(message=f"修改成功,下次运行时间{job_time}", data=await models.Task_Pydantic.from_queryset_single(models.Task.get(id=t_id)))
    except Exception as e:
        return core.Fail(message=f"修改失败.{e}")


@tasks.post("/task/{t_id}/run", name="立即运行测试任务")
async def run(t_id: int):
    data = await run_case(t_id)
    return core.Success(data={"id": data})


@tasks.post("/task/{t_id}/background", name="后台运行测试任务")
async def background_run(t_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_case, t_id)
    return core.Success(message="测试任务在后台运行中, 请稍后前往报告管理查看报告")


@tasks.get("/job/{j_id}", name="查看定时任务信息")
async def get(j_id: int):
    result = scheduler.get_job(str(j_id))
    return core.Success(data=str(result))
