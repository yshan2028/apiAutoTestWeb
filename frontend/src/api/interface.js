/**
 * 项目相关接口
 */
import request from "@/utils/request";

export function fetchList(query) {
  return request({
    url: "/interface",
    method: "get",
    params: query
  });
}

export function fetchInterface(id) {
  return request({
    url: "/interface",
    method: "get",
    params: { id }
  });
}

export function createInterface(data) {
  return request({
    url: "/interface",
    method: "post",
    data
  });
}

export function updateInterface(data) {
  return request({
    url: `/interface/${data.id}`,
    method: "put",
    data: {
      name: data.name,
      method: data.method,
      project_id: data.project_id,
      path: data.path,
      desc: data.desc,
      standard: data.standard
    }
  });
}

export function deleteInterface(id) {
  /**
   * 删除项目接口
   * params: id  项目id
   */
  return request({
    url: `/interface/${id}`,
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

// 导入接口
export function importInterfaces(data) {
  return request({
    url: "/interface/export",
    method: "post",
    data: {
      project_id: data.project_id,
      standard: data.standard,
      url: data.url,
      file: data.file
    }
  });
}
