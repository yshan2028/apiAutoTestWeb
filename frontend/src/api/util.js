import request from "@/utils/request";
/**
 * 使用说明 api
 * @returns
 */

export function help_doc() {
  return request({
    url: "/help"
  });
}

export function get_code() {
  return request({
    url: "/code"
  })
}

export function put_code(code){
  return request({
    url: "/code",
    method: "put",
    data: {code}
  })
}