/***
 * @Description: 实现每隔一秒打印 1,2,3,4
 * @Author: Harry
 * @Date: 2021-10-10 09:15:36
 * @Url: https://u.mr90.top
 * @github: https://github.com/rr210
 * @LastEditTime: 2021-10-10 09:31:52
 * @LastEditors: Harry
 */
// function printNum(num, delay, callback) {
//   setTimeout(() => {
//     for (i = 0; i < num; i++) {
//       console.log(i + 1);
//     }
//     callback()
//   }, delay)
// }

// const a = () => { printNum(4, 3000, a) }
// a()

// 使用闭包实现
// for (var i = 0; i < 4; i++) {
//   (function (i) {
//     setTimeout(function () {
//       console.log(i + 1);
//     }, i * 1000);
//   })(i);
// }

function makeFunc() {
  var name = "Mozilla";
  function displayName() {
      console.log(name);;
  }
  return displayName;
}

var myFunc = makeFunc();
myFunc();