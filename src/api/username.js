import request from '@/utils/request'

// 添加用户信息
export function createUserInfo(data) {
  // console.log('hanshu')
  return request({
    url: '/users/register',
    method: 'post',
    data
  })
}

// 获取所有用户信息
export function getUsersInfo() {
  return request({
    url: '/users/list',
    method: 'get'
  })
}

// 更新用户信息
export function UpdateUserInfoById(id, data) {
  return request({
    url: '/users/' + id,
    method: 'put',
    data
  })
}

// 删除用户信息
export function DeleteUserInfoById(id) {
  return request({
    url: '/users/' + id,
    method: 'delete'
  })
}

