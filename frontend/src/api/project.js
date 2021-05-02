/**
 * 项目相关接口
 */
import request from "@/utils/request";

export function fetchList(query) {
  return request({
    url: "/project",
    method: "get",
    params: query
  });
}

export function fetchProject(id) {
  return request({
    url: "/project",
    method: "get",
    params: { id }
  });
}

export function createProject(data) {
  return request({
    url: "/project",
    method: "post",
    data
  });
}

export function updateProject(data) {
  return request({
    url: `/project/${data.id}`,
    method: "put",
    data: { name: data.name, desc: data.desc }
  });
}

export function deleteProject(id) {
  /**
   * 删除项目接口
   * params: id  项目id
   */
  return request({
    url: `/project/${id}`,
    method: `delete`
  });
}
