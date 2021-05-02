#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: apiAutoTestFastAPI
@File  :__init__.py.py
@Author:zy7y
@Date  :2021/4/19 21:20
@Desc  :
"""

from fastapi import APIRouter, Depends

import core
from .case import cases

from .env import envs
from .inteface import interfaces
from .report import reports
from .task import tasks
from .user import users
from .project import projects
from .util import utils

v1 = APIRouter(prefix="/v1", dependencies=[Depends(core.get_current_user)])


# v1 = APIRouter(prefix="/v1")
v1.include_router(users)
v1.include_router(projects)
v1.include_router(envs)
v1.include_router(interfaces)
v1.include_router(cases)
v1.include_router(tasks)
v1.include_router(reports)
v1.include_router(utils)
