/*
 * @Author: zy7y
 * @Date: 2021-05-22 15:54:24
 * @LastEditTime: 2021-05-23 21:56:32
 * @LastEditors: Please set LastEditors
 * @Description: 用例相关接口
 * @FilePath: \frontend\src\api\case.js
 */

import request from "@/utils/request";

/**
 * @description: 分页获取用例数据
 * @param {*} query ： 分页条件 
 * @return {*}
 */
export function fetchList(query) {
  return request({
    url: "/case",
    method: "get",
    params: query
  });
}

/**
 * @description: 获取用例详细
 * @param {*} id： 用例id
 * @return {*}
 */
export function fetchCase(id) {
  return request({
    url: "/case",
    method: "get",
    params: { id }
  });
}

/**
 * @description: 创建用例
 * @param {*} data
 * @return {*}
 */
export function createCase(data) {
  return request({
    url: "/case",
    method: "post",
    data
  });
}

/**
 * @description: 更新用例
 * @param {*} data
 * @return {*}
 */
export function updateCase(data) {
  return request({
    url: `/case/${data.id}`,
    method: "put",
    data: {
      name: data.name,
      body: data.body,
      interface_id: data.interface_id,
      content_type: data.content_type,
      extra: data.extra,
      expect: data.expect,
      query: data.query,
      backend_sql: data.backend_sql
    }
  });
}

export function deleteCase(id) {
  /**
   * 删除项目接口
   * params: id  项目id
   */
  return request({
    url: `/case/${id}`,
    method: `delete`
  });
}

//  获取所有项目，部不分页
export function projectList() {
  return request({
    url: "/projects",
    method: "get"
  });
}

export function fetchInterface(id) {
  return request({
    url: `/interface/${id}`,
    method: "get"
  });
}
