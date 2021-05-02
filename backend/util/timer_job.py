#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: apiAutoTestFastApi
@File  :timer_job.py
@Author:zy7y
@Date  :2021/4/30 13:40
@Desc  : 定时任务, 写在内存中，参考文章 https://www.cnblogs.com/zhangliang91/p/12468871.html
https://blog.csdn.net/sunnyzyq/article/details/98597252
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import utc


class TimerJob:
    _scheduler = None

    def __init__(self):
        self._scheduler = AsyncIOScheduler()
        self._scheduler.configure(timezone=utc)  # utc作为调度程序的时区

    def init_timer(self):
        print("启动调度器...")
        self._scheduler.start()

    def close_timer(self):
        self._scheduler.shutdown(wait=True)
        print("关闭调度器...")

    def new_job(
            self,
            j_id: str,
            func: object,
            args: tuple,
            cron: str):
        """添加定时任务"""
        return self._scheduler.add_job(
            id=j_id, func=func, args=args, trigger=CronTrigger.from_crontab(cron))

    def delete_job(self, j_id: str):
        """删除定时任务"""
        return self._scheduler.remove_job(job_id=j_id)

    def stop_job(self, j_id: str):
        """暂停任务"""
        return self._scheduler.pause_job(job_id=j_id)

    def replay_job(self, j_id: str):
        """恢复任务"""
        return self._scheduler.resume_job(job_id=j_id)

    def modify_job(
            self,
            j_id: str,
            func: object,
            args: tuple,
            cron: str):
        """更新任务"""
        return self._scheduler.modify_job(
            job_id=j_id, func=func, args=args, trigger=CronTrigger.from_crontab(cron))

    def get_job(self, j_id: str):
        """获取定时任务信息"""
        return self._scheduler.get_job(job_id=j_id)

    def get_all(self):
        """所有任务"""
        self._scheduler.get_jobs()


scheduler = TimerJob()
