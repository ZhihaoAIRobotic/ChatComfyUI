import base64
from typing import Union
from fastapi import FastAPI
from comfy_client import ComfyClient
from comfyui_graph.comfy_graph import *
from utils.utils import load_config
import json

config = load_config('config/config.yml')
path_to_ComfyUI_output = config['path_to_ComfyUI_output']
path_to_ComfyUI_input = config['path_to_ComfyUI_input']
app = FastAPI()
client = ComfyClient(input_dir=path_to_ComfyUI_input, output_dir=path_to_ComfyUI_output)

@app.get("/text2img/")
def text2img(prompt, negative_prompt):
    with open('workflow/workflow_text2img_api.json', 'r') as file:
        graph = json.loads(file.read())
    comfy_graph = ComfyGraphText2img(graph=graph)
    comfy_graph.set_prompt(prompt=prompt, negative_prompt=negative_prompt, text_prompt_nodes=['3'])
    output = client.get_images(graph=comfy_graph.graph)
    return {"url": output}

@app.get("/img2img/")
def img2img(prompt, negative_prompt, image_name, image):
    image_data = base64.b64decode(image)
    with open('{}/{}'.format(client.input_dir, image_name), 'wb') as file:
        file.write(image_data)
    with open('workflow/workflow_img2img_api.json', 'r') as file:
        graph = json.loads(file.read())
    comfy_graph = ComfyGraphImg2img(graph=graph)
    comfy_graph.set_prompt(prompt=prompt, negative_prompt=negative_prompt,
                           text_prompt_nodes=['3'], image_path=image_name, image_prompt_nodes=['12'])
    output = client.get_images(graph=comfy_graph.graph)
    return {"url": output}

@app.get("/text2video")
def text2video(prompt, negative_prompt):
    with open('workflow/workflow_text2video_api.json', 'r') as file:
        graph = json.loads(file.read())
    comfy_graph = ComfyGraphText2video(graph=graph)
    comfy_graph.set_prompt(prompt='A boat sailing leisurely along the Seine River with the Eiffel Tower in background by Vincent van Gogh, blue sky',
                           negative_prompt='text, watermark', text_prompt_nodes=['17'])
    out_put = client.get_video_webp(comfy_graph.graph)
    return {"url": out_put}


