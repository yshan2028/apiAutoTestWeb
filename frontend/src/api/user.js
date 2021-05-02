import request from "@/utils/request";


// 本地接口的
export function login(data) {
  return request({
    url: "/login",
    method: "post",
    data
  });
}

export function getInfo() {
  return request({
    url: "/info",
    method: "get"
  });
}

export function logout() {
  return request({
    url: "/logout",
    method: "post"
  });
}

export function list(){
  return request({
    url: "/list"
  })
}