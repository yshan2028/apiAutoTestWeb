"""
project: apiAutoTestWeb
file: schemas.py
author: zy7y
date: 2021/4/17
"""
from typing import Any

from fastapi import Body
from pydantic.main import BaseModel


class ResponseBase(BaseModel):
    code: int = 200
    message: str = "请求成功."
    data: Any = None


class Success(ResponseBase):
    pass


class Fail(ResponseBase):
    code: int = 400
    message: str = "请求错误."


class Token(BaseModel):
    # access_token: str
    token: str
    token_type: str = "bearer"


class Login(BaseModel):
    username: str
    password: str


class Code(BaseModel):
    code: str


class TimerJob(BaseModel):
    job_id: str
    cron: str = Body(default='*/2 * * * *', max_length=30)  # 每2秒执行一次.


class ExportInterface(BaseModel):
    project_id: int
    url: str
    standard: str = "restful"
    file: Any = None


class MysqlSettings(BaseModel):
    host: str
    port: str
    user: str
    password: str
    database: str
