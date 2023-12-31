import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/users/login',
    method: 'post',
    data
  })
}
export function newpasswd(data) {
  return request({
    url: '/users/newpasswd',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/users/result',
    method: 'get',
    headers: {
      Authorization: 'Bearer ' + token
    }
  })
}

export function logout() {
  return request({
    url: '/vue-element-admin/user/logout',
    method: 'post'
  })
}
