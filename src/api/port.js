import request from '@/utils/request'

// 添加作者信息
export function createTaskInfo(data) {
  return request({
    url: '/portscan/task',
    method: 'post',
    data
  })
}
