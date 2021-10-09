/***
 * @Description: 
 * @Author: Harry
 * @Date: 2021-10-09 16:44:04
 * @Url: https://u.mr90.top
 * @github: https://github.com/rr210
 * @LastEditTime: 2021-10-09 17:07:55
 * @LastEditors: Harry
 */
let source = [
  {
    id: 1,
    pid: 0,
    name: 'body'
  }, {
    id: 2,
    pid: 1,
    name: 'title'
  }, {
    id: 3,
    pid: 2,
    name: 'div'
  }
]
function etree(arr) {
  let a = [...arr]
  for (let i = arr.length - 1; i > 0; i--) {
    if (arr[i].pid == arr[i - 1].id) {
      let b = arr[i-1]['children'] = a.pop()
    }
  }
  console.log(a);
}

etree(source)