const Mock = require("mockjs");
let data = Mock.mock({
  'number|0-2': 3
})
Mock.mock('http://localhost:8080/api/mock', 'post', () => { //三个参数。第一个：路径，第二个：请求方式post/get，第三个：回调，返回值

  return data
})
