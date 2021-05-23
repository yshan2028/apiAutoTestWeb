"""
project: apiAutoTestWeb
file: models.py
author: zy7y
date: 2021/4/17
"""
from typing import List

from tortoise import fields, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from .enum_filed import ContentType, Methods, Standard


# 抽象模型类
class AbstractModel(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(255, description="名称")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractModel):
    username = fields.CharField(max_length=255, unique=True, description="用户名")
    password = fields.CharField(max_length=255, description="用户密码")
    avatar = fields.CharField(
        max_length=255,
        default="/static/default.jpg",
        description="用户头像")


class Project(AbstractModel):
    name = fields.CharField(max_length=255, description="项目名称", unique=True)
    desc = fields.TextField(description="项目描述", null=True)

    # 查询集最大递归层级
    class PydanticMeta:
        max_recursion = 1


class Env(AbstractModel):
    base_url = fields.CharField(255, description="基准地址", unique=True)
    desc = fields.TextField(description="描述信息", null=True)
    base_header = fields.TextField(
        description="基准请求头", null=True, default='{}')
    # allow_none 生成的pydantic模型可以不传递该参数, default 可以设置数据库表中的默认值，pydantic的默认值
    db_settings = fields.JSONField(null=True, default=None, description="数据库配置")
    # 外键关联project表，可通过.envs访问到项目所有表
    # https://tortoise-orm.readthedocs.io/en/latest/models.html
    project = fields.ForeignKeyField('models.Project', related_name='envs')

    class PydanticMeta:
        max_recursion = 2


# 接口表
class Interface(AbstractModel):
    desc = fields.TextField(description="描述信息", null=True)
    path = fields.CharField(255, description="接口路径", null=True, default="")
    standard = fields.CharEnumField(
        Standard,
        description="使用规范",
        default=Standard.RESTFUL)
    method = fields.CharEnumField(
        Methods,
        description="请求方法",
        default=Methods.GET)
    project = fields.ForeignKeyField(
        'models.Project', related_name='Interfaces')

    class PydanticMeta:
        max_recursion = 2


class Case(AbstractModel):
    name = fields.CharField(max_length=255, description="用例名称", unique=True)
    content_type = fields.CharEnumField(
        ContentType,
        description="参数类型",
        default=ContentType.PARAMS)
    # graphql 规范的请求体
    query = fields.TextField(
        description="graphql query语句",
        null=True,
        default=None)
    # 请求参数
    body = fields.TextField(
        description="请求参数",
        null=True,
        allow_none=True,
        default=None)
    extra = fields.CharField(
        255,
        description="从接口响应提取参数",
        null=True,
        allow_none=True,
        default=None)
    # 后置sql
    backend_sql = fields.TextField(description="后置sql", default="", null=True, allow_none=True)
    expect = fields.TextField(description="预期结果", default='{}')
    interface = fields.ForeignKeyField(
        'models.Interface',
        related_name='Cases',
        description="所属接口")

    class PydanticMeta:
        max_recursion = 2


class Task(AbstractModel):
    name = fields.CharField(max_length=255, description="任务名称", unique=True)
    env = fields.ForeignKeyField('models.Env', related_name='task_env')
    cases = fields.ManyToManyField('models.Case', related_name='Tasks')
    is_timer = fields.BooleanField(default=False, description="定时任务开关")
    cron = fields.CharField(
        255,
        description="cron表达式",
        null=True,
        default=None)

    class PydanticMeta:
        max_recursion = 1


class Report(AbstractModel):
    data = fields.JSONField(description="报告内容")
    tasks = fields.ForeignKeyField('models.Task', related_name='Reports')
    start = fields.CharField(description="测试开始时间", max_length=255)
    end = fields.CharField(description="测试结束时间", max_length=255)

    class PydanticMeta:
        max_recursion = 1


# 解决pydantic_model_creator 生成的模型中 缺少外键关联字段
Tortoise.init_models(["db.models"], "models")

# 返回模型
User_Pydantic = pydantic_model_creator(User, name="User", exclude=["password"])

# 输入模型 exclude_readonly 只读字段 非必填
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude=[
                                         "avatar"], exclude_readonly=True)

Project_Pydantic = pydantic_model_creator(Project, name="Project")
ProjectIn_Pydantic = pydantic_model_creator(
    Project, name="ProjectIn", exclude_readonly=True)

Env_Pydantic = pydantic_model_creator(Env, name="Env")
EnvIn_Pydantic = pydantic_model_creator(
    Env, name="EvnIn", exclude_readonly=True)

Interface_Pydantic = pydantic_model_creator(Interface, name="Interface")
InterfaceIn_Pydantic = pydantic_model_creator(
    Interface, name="InterfaceIn", exclude_readonly=True)

Case_Pydantic = pydantic_model_creator(Case, name="Case")
CaseIn_Pydantic = pydantic_model_creator(
    Case, name="CaseIn", exclude_readonly=True)

Task_Pydantic = pydantic_model_creator(Task, name="Task")
TaskIn_Pydantic = pydantic_model_creator(
    Task, name="TaskIn", exclude_readonly=True)


class TaskInCase(TaskIn_Pydantic):
    case_list: List[int]


Report_Pydantic = pydantic_model_creator(Report, name='Report')
ReportIn_Pydantic = pydantic_model_creator(
    Report, name="ReportIn", exclude_readonly=True)
