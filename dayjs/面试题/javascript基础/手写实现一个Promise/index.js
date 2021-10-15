/***
 * @Description: 
 * @Author: Harry
 * @Date: 2021-10-15 11:20:07
 * @Url: https://u.mr90.top
 * @github: https://github.com/rr210
 * @LastEditTime: 2021-10-15 16:36:39
 * @LastEditors: Harry
 */
// let _this;
// class Hd {
//   static PENDING = 'pending'
//   static FULFILLED = 'fulfilled'
//   static REJECTED = 'rejected'
//   constructor(params) {
//     this.static = Hd.PENDING
//     this.value = null
//     _this = this
//     params(this.reslove, this.reject)
//   }
//   reslove(value) {
//     if (_this.value === Hd.PENDING) {
//       _this.static = Hd.FULFILLED
//       _this.value = value
//     }
//   }
//   reject(reason) {
//     if (_this.value === Hd.PENDING) {
//       _this.static = Hd.REJECTED
//       _this.value = reason
//     }
//   }
// }

class Hd {
  static PENDING = 'pending'
  static FULFILLED = 'fulfilled'
  static REJECTED = 'rejected'
  constructor(params) {
    this.static = Hd.PENDING
    this.value = null
    this.callback = []
    try {
      params(this.reslove.bind(this), this.reject.bind(this))
    } catch (error) {
      this.reject(error)
    }
  }
  reslove(value) {
    if (this.static === Hd.PENDING) {
      this.static = Hd.FULFILLED
      this.value = value
      setTimeout(() => {
        this.callback.forEach(v => {
          // console.log(v.OnFulfilled(value));
          v.OnFulfilled(value);
        })
      })
    }
  }
  reject(reason) {
    if (this.static === Hd.PENDING) {
      this.static = Hd.REJECTED
      this.value = reason
      setTimeout(() => {
        this.callback.forEach(v => {
          v.OnRejected(reason);
        })
      })
    }
  }
  then(OnFulfilled, OnRejected) {
    if (typeof OnFulfilled !== 'function') {
      OnFulfilled = () => this.value
    }
    if (typeof OnRejected !== 'function') {
      // console.log(this.value);
      OnRejected = () => this.value
    }
    return new Hd((reslove, rejcet) => {
      // 进行判断 当当前的promise状态为fulfilled时 执行以上onFulfilled函数
      // 对pending状态进行判断
      if (this.static === Hd.PENDING) {
        // 对准备阶段的错误进处理
        this.callback.push({
          OnFulfilled: (value) => {
            try {
              OnFulfilled(value)
            } catch (error) {
              OnRejected(error)
            }
          },
          OnRejected: () => {
            try {
              OnRejected(value)
            } catch (error) {
              OnRejected(error)
            }
          }
        })
      }
      if (this.static === Hd.FULFILLED) {
        // 这里要实现异步执行 使用宏任务进行 延时操作
        // console.log(this.value);
        setTimeout(() => {
          try {
            let result = OnFulfilled(this.value)
            reslove(result)
          } catch (error) {
            rejcet(error)
          }
        })
      }
      if (this.static === Hd.REJECTED) {
        setTimeout(() => {
          try {
            let result = OnRejected(this.value)
            reslove(result)
          } catch (error) {
            rejcet(error)
          }
        })
      }
    })
  }
}