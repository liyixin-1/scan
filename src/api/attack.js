import request from '@/utils/request'

// 添加作者信息
export function createTaskInfo(data) {
  // console.log(data)
  return request({
    url: '/attack/task',
    method: 'post',
    data
  })
}
export function getAttackInfo(attacktype) {
  console.log(attacktype)
  return request({
    url: '/attack/result/' + attacktype,
    method: 'get',
    // params: { attacktype }
  })
}
