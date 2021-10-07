/***
 * @Description: 
 * @Author: Harry
 * @Date: 2021-10-06 19:58:33
 * @Url: https://u.mr90.top
 * @github: https://github.com/rr210
 * @LastEditTime: 2021-10-06 19:59:45
 * @LastEditors: Harry
 */

let _ = require('./loadsh.js')
var obj1 = {
  a: 1,
  b: { f: { g: 1 } },
  c: [1, 2, 3]
};
var obj2 = _.cloneDeep(obj1);
console.log(obj1.b.f === obj2.b.f);// false