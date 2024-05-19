import axios from 'axios';

// 定义后端API的URL
const apiUrl = 'http://localhost:3001/text2img';


export default async function handler(req, res) {
    try {
        // 移除无关的变量
        req.body = Object.entries(req.body).reduce(
        (a, [k, v]) => (v == null ? a : ((a[k] = v), a)),
        {}
        );

        // 从前端请求中获取参数
        const { prompt } = req.body;
  
        // 构建要传递的参数对象
        const requestData = {
        param: prompt,
        };
  
      // 发起带参数的GET请求到FastAPI的API
      const response = await axios.get(apiUrl, {
        params: requestData,
        headers: {
          "Content-Type": "application/json",
        },
      });
  
      if (response.status !== 200) {
        const error = response.data;
        res.statusCode = 500;
        res.end(JSON.stringify({ detail: error.detail }));
        return;
      }
  
      const prediction = response.data;
      res.end(JSON.stringify(prediction));
    } catch (error) {
      console.error('请求时出错:', error);
      res.statusCode = 500;
      res.end(JSON.stringify({ detail: '请求时出错' }));
    }
  }

  

export const config = {
  api: {
    bodyParser: {
      sizeLimit: "10mb",
    },
  },
};