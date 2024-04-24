## HOW TO RUN SERVER

1. make model dir

   ```
   mkdir model
   ```

2. download diffussion model

   ```
   cd model
   wget https://civitai.com/api/download/models/393286
   mv 393286 Ath_stuffed-toy_XL.safetensors
   wget https://civitai.com/api/download/models/126601
   mv 126601 sdXL_v10.safetensors
   ```

3. run the server

   ```
   uvicorn main:app --reload
   ```

   you can access the server via **http://127.0.0.1:8000** 