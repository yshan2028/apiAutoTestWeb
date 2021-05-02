import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

/* Layout */
import Layout from "@/layout";

/**
*注：子菜单仅在布线时出现儿童长度>= 1
*详见：https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
*hidden:true如果设置为true，项目将不会显示在侧边栏中（默认为false）
*alwaysShow:true如果设置为true，将始终显示根菜单
*如果未设置alwaysShow，则当项目有多个子路由时，
*它将变成嵌套模式，否则不显示根菜单
*重定向：noRedirect如果设置noRedirect将不会在breadcrumb中重定向
*名称：'router-name'名称由<keep alive>使用（必须设置！！！）
*元：{
角色：['admin'，'editor']控制页面角色（可以设置多个角色）
title:'title'侧边栏和面包屑中显示的名称（推荐设置）
icon:'svg name'/'el-icon-x'侧边栏中显示的图标
breadcrumb:false如果设置为false，则项目将隐藏在breadcrumb中（默认为true）
activeMenu:“/example/list”如果设置路径，侧边栏将突出显示您设置的路径
}
*/

/**
 * constantRoutes
 * 没有权限要求的基页
 * 可以访问所有角色
 */
export const constantRoutes = [
  {
    path: "/login",
    component: () => import("@/views/login/index"),
    hidden: true // 不需要显示在导航栏上
  },
  
  {
    path: "/404",
    component: () => import("@/views/404"),
    hidden: true
  },

  {
    path: "/",
    component: Layout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        // 面包屑导航显示内容
        name: "Dashboard",
        component: () => import("@/views/dashboard/index"),
        //  title 左侧导航显示的名称 icon 左侧显示的图标
        meta: { title: "运营统计", icon: "el-icon-house" }
      }
    ]
  },

  // 使用说明前端路由
  {
    path: "/help",
    component: Layout,
    children: [
      {
        path: "index",
        // 面包屑导航显示内容
        name: "Help",
        component: () => import("@/views/help/index"),
        //  title 左侧导航显示的名称 icon 左侧显示的图标
        meta: { title: "使用说明", icon: "el-icon-reading" }
      }
    ]
  },

  // 项目管理前端路由
  {
    path: "/project",
    component: Layout,
    children: [
      {
        path: "index",
        component: () => import("@/views/project/index"),
        name: "Project",
        meta: { title: "项目管理", icon: "el-icon-data-analysis" }
      }
    ]
  },

  // 环境管理前端路由
  {
    path: "/env",
    component: Layout,
    children: [
      {
        path: "index",
        component: () => import("@/views/env/index"),
        name: "Env",
        meta: { title: "环境管理", icon: "el-icon-c-scale-to-original" }
      }
    ]
  },

  // 接口管理前端路由
  {
    path: "/interface",
    component: Layout,
    children: [
      {
        path: "index",
        component: () => import("@/views/interface/index"),
        name: "Api",
        meta: { title: "接口管理", icon: "el-icon-link" }
      }
    ]
  },

  // 用例管理前端路由
  {
    path: "/case",
    component: Layout,
    children: [
      {
        path: "/index",
        component: () => import("@/views/case/index"),
        name: "Case",
        meta: { title: "用例管理", icon: "el-icon-suitcase" }
      }
    ]
  },

  // 任务管理前端路由
  {
    path: "/task",
    component: Layout,
    children: [
      {
        path: "index",
        component: () => import("@/views/task/index"),
        name: "Task",
        meta: { title: "任务管理", icon: "el-icon-timer" }
      },
      {
        path: "edit",
        name: "edit",
        component: () => import("@/views/task/create.vue"),
        hidden: true // (默认 false)
      },
      {
        path: "add",
        name: "add",
        component: () => import("@/views/task/create.vue"),
        hidden: true // (默认 false)
      }
    ]
  },

  // 报告管理前端路由
  {
    path: "/report",
    component: Layout,
    children: [
      {
        path: "index",
        component: () => import("@/views/report/index"),
        name: "Report",
        meta: { title: "报告管理", icon: "el-icon-document-checked" }
      },
      {
        path: "info",
        component: () => import("@/views/report/info"),
        name: "info",
        meta: { title: "报告详细", icon: "el-icon-document-checked" },
        hidden: true // (默认 false)
      }
    ]
  },


  // 扩展脚本前端路由
  {
    path: "/code",
    component: Layout,
    children: [
      {
        path: "index",
        component: () => import("@/views/code/index"),
        name: "Code",
        meta: { title: "扩展脚本", icon: "el-icon-cpu" }
      }
    ]
  },
   // 扩展脚本前端路由
   {
    path: "/tools",
    component: Layout,
    meta: { title: "小工具", icon: "el-icon-s-tools" },
    children: [
      {
        path: "json",
        component: () => import("@/views/tools/json"),
        name: "Json",
        meta: { title: "Json校验", icon: "el-icon-s-tools" }
      },
      // {
      //   path: "postman",
      //   component: () => import("@/views/tools/index"),
      //   name: "Postman",
      //   meta: { title: "简易Postman", icon: "el-icon-thumb" }
      // }
    ],
  },


  {
    path: "external-link",
    component: Layout,
    meta: {title: "源码获取", icon: "link"},
    children: [
      {
        path: "https://gitee.com/zy7y/apiAutoTestFastApi.git",
        meta: { title: "后端源码", icon: "link" }
      },
      {
        path: "https://gitee.com/zy7y/apiAutoTestVue.git",
        meta: { title: "前端源码", icon: "link" }
      },
      {
        path: "https://gitee.com/zy7y/apiAutoTestWeb.git",
        meta: { title: "apiAutoTestWeb", icon: "link" }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: "*", redirect: "/404", hidden: true }
];

const createRouter = () =>
  new Router({
    mode: 'history', // require service support
    scrollBehavior: () => ({ y: 0 }),
    routes: constantRoutes
  });

const router = createRouter();

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter();
  router.matcher = newRouter.matcher; // reset router
}

export default router;
