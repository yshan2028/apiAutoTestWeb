#  apiAutoTestWeb使用说明

> [apiAutoTestWeb](https://gitee.com/zy7y/apiAutoTestWeb)是为apiAutoTest的可视化版本，其采用前后端分离([FastAPI](https://fastapi.tiangolo.com/) + [Vue2](https://cn.vuejs.org/))方式实现
>
> 具体使用: Python3 + FastAPI + Vue + element-ui + vue element admin + Tortoise ORM + jwt(python-jose) + apscheduler + aiohttp + aiofiles + jsonpath

# 演示地址

==**http://49.232.203.244:2152/**==

点击即可访问: [前端入口](http://49.232.203.244:2152/), [接口文档](http://49.232.203.244:1338/docs)

# 目的

> 尝试将学了一年FastAPI 和Vue 做个结合,动手做才能更快的获得知识，在做的时候基本是遇到什么问题就查，最终出来了这一版本.

# 相比apiAutoTest

1. header支持使用自定义函数以及其他接口参数变量

   > 弊端: 将无法再对单个用例不使用header或者单独使用header，为此移除了token操作

2. 增加了定时任务， 后台运行

3. 支持[graphql](https://graphql.cn/)规范接口测试

4. 将excel数据托管到可视化界面和数据库管理

   > 弊端: 感觉更繁琐了，需要不停的在页面切换

5. 暂不支持SQL

   >tip: 不排除自定义函数中可以使用sql

6. 扩展函数

   > 不支持，安装第三方库

7. 前端表单填写采用文本域，没法校验是否有问题

8. 上传文件接口暂不支持

# 功能介绍

## 1. 登录

![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502102037287.png)

- 页面并没有写注册入口, 暂时只能通过接口来注册.
- 默认的演示账号: tester 密码: 123456

## 2. 首页

![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502115916433.png)

## 3. 说明文档

![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502115930597.png)

## 4. 项目管理

![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502103059858.png)

## 5. 环境管理

![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502103630089.png)

- 基准header, 类似JSON的写法`{"Authorization":"${token}"}`欲使用token，当token变量存在的时候会自动给其替换，其他接口(在token提取接口之后的)将被自动使用， 其具体效果见`报告详细`, `变量知识(见用例模块)`
- 当然也可以使用`自定义函数`来解决下面的问题

![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502104011903.png)

## 6. 接口管理

- [RESTful规范](https://www.runoob.com/w3cnote/restful-architecture.html)

  > 也实用一般的http/https(带证书暂未测试，应该不支持)接口

  ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502104436160.png)

  路径可以使用`自定义函数`、`参数变量`

  ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502110622127.png)

- [GraphQL规范](https://graphql.cn/)

  > 目前个人公司项目接触到，发现只能是post请求，json数据格式传输

  ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502104458705.png)
  
- 接口导入(2020-05-03新增)

  > 该版本仅支持通过Swagger接口文档(openapi.json)`url`方式导入，暂不支持用例生成.

  ![](https://gitee.com/zy7y/blog_images/raw/master/img/20210503221628.png)

  - `openapi.json`地址获取

    ![](https://gitee.com/zy7y/blog_images/raw/master/img/20210503222116.png)
## 7. 用例管理

- RESTful规范

  ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502105234223.png)

- 参数类型: 根据接口文档选择
- 请求参数: 类json(`只所以说是类json写法是因为后面有些地方使用非字符串的参数时会有是不合法json的情况`)写法, 可以使用`自定义函数`,`参数变量`
- 预期结果: `{"$.meta":{ "msg": "登录成功", "status": 200 }}`，`$.meta` 实际结果(`将会通过jsonpath对当前接口的响应提取内容$.meta为jsonpath表达式，意为从当前响应json中提取第一层级为key为meta的内容`),`{ "msg": "登录成功", "status": 200 }`预期结果内容, 支持多个预期结果，添加多个键值对即可
- 提取参数: `{"token":"$.data.token"}`, `token`为参数变量，`$.data.token`从当前接口响应提取token的值并赋值给自定义变量token,  如果已经存在变量token，那么这个token 会覆盖之前的变量token内容，

- GraphQL规范： 除了query语句部分不同，其他一致

  ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502110248043.png)

## 8. 任务管理

![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502112453362.png)

- 立即执行:  必须等待执行完成之后，自动跳转报告信息，且无法在测试过程中去做其他操作
- 后台执行：任务将在后台运行，需要执行去报告管理查看，然后可以去做其他操作
- 定时信息：展示该任务的定时信息，会显示下次运行时间
- 删除: 会删除任务以及定时任务

![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502112437202.png)

- 选择用例：需先选择对应的环境，然后此处可以选择对应项目下的所有用例，`已选中用例的展示顺序，将决定接口依次运行的顺序，会直接影响到每个接口变量参数的使用`，你应该在使用变量参数前执行提取该变量参数的接口

- 定时任务：目前定时任务是写在内存中的，每次应用重启，已有的定时任务都会失效

  > 可通过，删除任务，编辑任务的定时任务开关来删除或者关闭定时任务

- 定时规则: 遵顼`cron`表达式示例给出的`* * * * *`意为每分钟执行一次任务

## 9. 报告管理

![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502112927615.png)

![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502113109583.png)

- 点击测试结果可筛选结果
- 点击首行的箭头展开查看详细

### 报告解读

1. 请求信息: `显示当前用例的请求前 VS 请求后的 数据处理`

   ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502113332567.png)

   ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502113451617.png)

2. 提取参数: `显示当前用例的提取参数表达式`

   ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502113524141.png)

3. 响应结果： `显示当前用例的响应结果`

   ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502113655236.png)

4. 断言信息：`显示当前用例的断言内容`

   > `$.meta ? {'msg': '登录成功', 'status': 200}` 用例中书写的预期结果内容
   >
   > `{'msg': '登录成功', 'status': 200} == {'msg': '登录成功', 'status': 200}` 处理后实际的预期结果内容

   ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502113835929.png)

5. 当前参数池：`显示当前用例运行之后的可用参数变量`

   ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502114225072.png)

6. 异常信息：`显示当前用例运行出现的异常信息`

   ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502114637048.png)

   > 关于异常的种类分析还需要统计后，也许后面会更新在文档上，目前如果出现异常请仔细查看`请求信息`，和`异常信息`等内容

   ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502114919036.png)

   ![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502115019284.png)

## 7. 扩展脚本

[![gZWbC9.png](https://z3.ax1x.com/2021/05/02/gZWbC9.png)](https://imgtu.com/i/gZWbC9)

> 每次编辑之后，需要保存才会生效，此处的函数仅能作用于 `接口path,用例请求参数、预期结果`中，不支持调试

## 8. Json校验

![](https://gitee.com/zy7y/blog_images/raw/master/img/image-20210502115624216.png)

> 提供了实时的json格式校验

# 参考资料

- Vue: https://cn.vuejs.org/

- Element-ui: https://element.eleme.cn/#/zh-CN/component/installation

- vue-element-admin: https://panjiachen.gitee.io/vue-element-admin-site/zh/

- FastAPI: https://fastapi.tiangolo.com/

- Tortoise ORM: https://tortoise-orm.readthedocs.io/en/latest/

  > 还有源码中注释的链接资料

# 最后

1. 感谢在此过程中我查过的所有资料的作者，提供答案的网友
2. 该项目作为一个`Demo`，任有很多`Bug`和冗余代码可以优化
3. 如果你有什么建议或者`Bug`反馈可以在[源码仓库](https://gitee.com/zy7y/apiAutoTestWeb.git)进行反馈
4. 如果你也想加入这个项目可以直接申请成为仓库成员
5. 如果你需要及时得到问题回复可以加入该QQ群`851163511`
6. 如果你觉得这个项目有点用处，有帮助到你，还请点个`star`
   - Gitee: https://gitee.com/zy7y/apiAutoTestWeb.git
   - Github: https://github.com/zy7y/apiAutoTestWeb.git
7. 视频过程
   - https://space.bilibili.com/438858333/channel/detail?cid=179917&ctype=0
   - RESTful接口流程演示：https://www.bilibili.com/video/BV1Q64y1y7oF
   - GraphQL接口流程演示：https://www.bilibili.com/video/BV1r84y1F7ew