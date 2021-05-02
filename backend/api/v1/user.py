"""
project: apiAutoTestWeb
file: user.py
author: zy7y
date: 2021/4/17
desc: 用户相关
"""

from fastapi import APIRouter, Depends

import core
from db import models

users = APIRouter(tags=["用户相关"])


@users.get("/info", name="获取当前登录用户信息")
async def info(user: models.UserIn_Pydantic = Depends(core.get_current_user)):
    """
    - token
    :return: 用户除密码外的信息
    """
    return core.Success(data=await models.User_Pydantic.from_tortoise_orm(user))


@users.post("/user", name="新增用户")
async def create(user: models.UserIn_Pydantic):
    """
    - name：str
    - username： str
    - password： str
    :return: 用户除密码外的信息
    """
    user.password = core.get_password_hash(user.password)
    user_obj = await models.User.create(**user.dict(exclude_unset=True))
    # from_tortoise_orm 从 数据表中序列化
    return core.Success(data=await models.User_Pydantic.from_tortoise_orm(user_obj))
