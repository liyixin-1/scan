import request from '@/utils/request'

// 添加作者信息
export function createTaskInfo(data) {
  console.log(data)
  return request({
    url: '/blowup/task',
    method: 'post',
    data
  })
}
