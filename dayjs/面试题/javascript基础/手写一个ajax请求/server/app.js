const express = require('express')
const app = express()
const bodyParser = require('body-parser')
// app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
// post请求体中的Content-Type为：application/json，则配置如下：
// 解决跨域的问题
app.all('*', function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  // res.header("Access-Control-Allow-Headers", "X-Requested-With");
  // res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
  // res.header("X-Powered-By",' 3.2.1')
  // res.header("Content-type", "application/json");
  next();
});
app.get('/user', function (req, res) {
  let { callback } = req.query
  if (callback) {
    res.setHeader('Content-type', 'application/javascript');
    res.send(callback + '({ message: "Get请求成功", code: 1 })')
  } else {
    res.send({ message: "Get请求成功", code: 1 })
  }
})

app.post('/user', (req, res) => {
  res.send({ message: "Post请求成功", code: 1 })
})

app.listen(3000, () => {
  console.log('服务器启动成功');
})