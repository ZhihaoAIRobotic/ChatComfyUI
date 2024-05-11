
export default async function handler(req, res) {
  const response = await fetch('/text2img', {
    headers: {
      "Content-Type": "application/json",
    },
  });
  
  if (response.status !== 200) {
    let error = await response.json();
    res.statusCode = 500;
    res.end(JSON.stringify({ detail: error.detail }));
    return;
  }

  const prediction = await response.json();
  res.end(JSON.stringify(prediction));
}
