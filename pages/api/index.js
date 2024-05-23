import axios from 'axios';


// 定义后端API的URL
const apiUrl = 'http://localhost:8001/text2img/';


export default async function handler(req, res) {
    try {
        req.body = Object.entries(req.body).reduce(
        (a, [k, v]) => (v == null ? a : ((a[k] = v), a)),
        {}
        );

        const { prompt } = req.body;

      const response = await axios.get(apiUrl, {
        params: {prompt: prompt},
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
      console.error('Error in request:', error);
      res.statusCode = 500;
      res.end(JSON.stringify({ detail: 'Error in request' }));
    }
  }

  

export const config = {
  api: {
    bodyParser: {
      sizeLimit: "10mb",
    },
  },
};