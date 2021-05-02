/**
 * 项目相关接口
 */
import request from "@/utils/request";

export function fetchList(query) {
  return request({
    url: "/env",
    method: "get",
    params: query
  });
}

export function fetchEnv(id) {
  return request({
    url: "/env",
    method: "get",
    params: { id }
  });
}

export function createEnv(data) {
  return request({
    url: "/env",
    method: "post",
    data
  });
}

export function updateEnv(data) {
  return request({
    url: `/env/${data.id}`,
    method: "put",
    data: {
      name: data.name,
      base_url: data.base_url,
      project_id: data.project_id,
      base_header: data.base_header,
      desc: data.desc
    }
  });
}

export function deleteEnv(id) {
  /**
   * 删除项目接口
   * params: id  项目id
   */
  return request({
    url: `/env/${id}`,
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
