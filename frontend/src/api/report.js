import request from "@/utils/request";

export function fetchList(query) {
  return request({
    url: "/report",
    method: "get",
    params: query
  });
}

export function fetchReport(id) {
    return request({
      url: `/report/${id}`,
      method: "get",
    });
  }


export function deleteReport(id) {
  /**
   * 删除项目接口
   * params: id  项目id
   */
  return request({
    url: `/report/${id}`,
    method: `delete`
  });
}