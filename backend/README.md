## HOW TO RUN SERVER

1. run ComfyUI server at http://127.0.0.1:8188/

2. download the models according to the workflow and put them in ComfyUI/model folder

3. edit the config/config.yml file according to the absolute path to the ComfyUI/input folder and absolute path to the ComfyUI/output folder

4. run the server

   ```
   uvicorn main:app --reload
   ```

you can access the server via http://127.0.0.1:8000/