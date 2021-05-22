/**
 * 项目相关接口
 */
import request from "@/utils/request";

export function fetchList(query) {
  return request({
    url: "/case",
    method: "get",
    params: query
  });
}

export function fetchCase(id) {
  return request({
    url: "/case",
    method: "get",
    params: { id }
  });
}

export function createCase(data) {
  return request({
    url: "/case",
    method: "post",
    data
  });
}

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
      query: data.query
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
