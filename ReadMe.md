# apiAutoTestWeb
> 基本为apiAutoTest使用FastAPI + Vue的前后端的分离版本，在apiAutoTest之上
> 实现了定时任务，自定义函数，接口参数依赖，graphql规范接口测试
# 演示环境
==**http://49.232.203.244:2152/**==

点击即可访问: [前端入口](http://49.232.203.244:2152/), [接口文档](http://49.232.203.244:1338/docs)
# 目前完善功能
- [x] 登录
- [x] 项目管理
- [x] 接口管理
- [x] 环境管理
- [x] 用例管理
- [x] 报告管理
- [x] 扩展脚本

# 文档资料
[apiAutoTestWeb说明文档](backend/apiAutoTestWeb使用说明.md)
[后端说明文档](backend/readme.md)
[前端说明文档](frontend/README.md)


# 部署
1. git clone https://gitee.com/zy7y/apiAutoTestWeb.git
2. 安装docker: https://www.cnblogs.com/zy7y/p/14344375.html
3. 安装docker-compose : https://blog.csdn.net/qq_36640395/article/details/107449652 需要安装Python3， 然后pip命令换成pip3
4. 修改`frontend/.env.production`文件中的`VUE_APP_BASE_API`为自己服务器的地址
5. 在apiAutoTestWeb目录下执行`构建镜像 docker-compose build 运行服务 docker-compose up -d`
6. 访问前端`IP:2152`, 访问接口文档`IP:1328`
## 参考资料
1. https://blog.csdn.net/qq_38225558/article/details/103068220
2. https://cli.vuejs.org/zh/guide/deployment.html#docker-nginx
3. https://www.cnblogs.com/xr210/p/12676811.html
# 最后

1. 感谢在此过程中我查过的所有资料的作者，提供答案的网友
2. 该项目作为一个`Demo`，任有很多`Bug`和冗余代码可以优化
3. 如果你有什么建议或者`Bug`反馈可以在[apiAutoTestWeb源码仓库](https://gitee.com/zy7y/apiAutoTestWeb.git)进行反馈
4. 如果你也想加入这个项目可以直接申请成为仓库成员
5. 如果你需要及时得到问题回复可以加入该QQ群`851163511`
6. 如果你觉得这个项目有点用处，有帮助到你，还请点个`star`
   - Gitee: https://gitee.com/zy7y/apiAutoTestWeb.git
   - Github: https://github.com/zy7y/apiAutoTestWeb.git
7. 视频过程
   - https://space.bilibili.com/438858333/channel/detail?cid=179917&ctype=0
   - RESTful接口流程演示：https://www.bilibili.com/video/BV1Q64y1y7oF
   - GraphQL接口流程演示：https://www.bilibili.com/video/BV1r84y1F7ew