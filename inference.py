from copy import deepcopy
from io import BytesIO
from urllib import request
import numpy
import os
from PIL import Image
import pytest
from pytest import fixture
import time
import torch
from typing import Union
import json
import subprocess
import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import urllib.request
import urllib.parse


from comfy.samplers import KSampler

"""
These tests generate and save images through a range of parameters
"""

class ComfyGraph:
    def __init__(self, 
                 graph: dict,
                 input_nodes: list[str],
                 ):
        self.graph = graph
        self.input_nodes = input_nodes

    def set_prompt(self, prompt, negative_prompt=None):
        # Sets the prompt for the sampler nodes (eg. base and refiner)
        # print(type(self.graph['prompt']))
        # choose the one in the dict list has a "id": 218
        i = 0
        self.graph['218']['inputs']['image'] = '/home/lzh/Desktop/geeks (3).jpg'

        # for node in self.input_nodes:
        #     print(self.graph[node])
        #     print(self.graph[node]['inputs'])
        #     prompt_node = self.graph[node]['inputs']['positive'][0]
        #     self.graph[prompt_node]['inputs']['text'] = prompt
        #     if negative_prompt:
        #         negative_prompt_node = self.graph[node]['inputs']['negative'][0]
        #         self.graph[negative_prompt_node]['inputs']['text'] = negative_prompt




class ComfyClient:
    # From examples/websockets_api_example.py

    def connect(self, 
                    listen:str = '127.0.0.1', 
                    port:Union[str,int] = 8188,
                    client_id: str = str(uuid.uuid4())
                    ):
        self.client_id = client_id

        self.server_address = f"{listen}:{port}"
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.server_address, self.client_id))
        print(f"Connected to {self.server_address}")
        print(f"Client ID: {self.client_id}")
        self.ws = ws

    def queue_prompt(self, prompt):
        print(self.ws)
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        print('sending prompt', data)
        req =  urllib.request.Request("http://{}/prompt".format(self.server_address), data=data)
        print(req)
        return json.loads(urllib.request.urlopen(req).read())

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}".format(self.server_address, url_values)) as response:
            return response.read()
        
    def get_video(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}".format(self.server_address, url_values)) as response:
            return response.read()

    def get_history(self, prompt_id):
        with urllib.request.urlopen("http://{}/history/{}".format(self.server_address, prompt_id)) as response:
            return json.loads(response.read())

    def get_images(self, graph, save=True):
        prompt = graph

        prompt_id = self.queue_prompt(prompt)['prompt_id']
        print(f"Prompt ID: {prompt_id}")
        output_images = {}
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break #Execution is done
            else:
                continue #previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        for o in history['outputs']:
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                print(f"Node output: {node_output}")
                if 'images' in node_output:
                    images_output = []
                    for image in node_output['images']:
                        image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                        images_output.append(image_data)
                output_images[node_id] = images_output

        return output_images
    
    def get_videos(self, graph, save=True):
        prompt = graph

        prompt_id = self.queue_prompt(prompt)['prompt_id']
        print(f"Prompt ID: {prompt_id}")
        output_images = {}
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break #Execution is done
            else:
                continue #previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        for o in history['outputs']:
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                print(f"Node output: {node_output}")
                
                if 'gifs' in node_output:
                    images_output = []
                    for image in node_output['gifs']:
                        image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                        images_output.append(image_data)
                output_images[node_id] = images_output

        return output_images



sampler_list = KSampler.SAMPLERS
scheduler_list = KSampler.SCHEDULERS

# @pytest.mark.inference
# @pytest.mark.parametrize("sampler", sampler_list)
# @pytest.mark.parametrize("scheduler", scheduler_list)
# @pytest.mark.parametrize("prompt", prompt_list)
class TestInference:
    #

    def start_client(self, listen:str, port:int):
        # Start client
        comfy_client = ComfyClient()
        # Connect to server (with retries)
        n_tries = 5
        for i in range(n_tries):
            time.sleep(4)
            try:
                comfy_client.connect(listen=listen, port=port)
            except ConnectionRefusedError as e:
                print(e)
                print(f"({i+1}/{n_tries}) Retrying...")
            else:
                break
        return comfy_client

    #
    # Client and graph fixtures with server warmup
    #
    # Returns a "_client_graph", which is client-graph pair corresponding to an initialized server
    # The "graph" is the default graph
    def _client_graph(self, comfy_graph) -> (ComfyClient, ComfyGraph):
        comfy_graph = comfy_graph
        
        # Start client
        comfy_client = self.start_client('127.0.0.1', '8188')

        # Warm up pipeline
        comfy_client.get_videos(graph=comfy_graph.graph, save=False)

        return comfy_client, comfy_graph


    def client(self, _client_graph):
        client = _client_graph
        return client
    
    def comfy_graph(self, _client_graph):
        # avoid mutating the graph
        graph = deepcopy(_client_graph)
        return graph

    def test_comfy(
        self,
        client,
        comfy_graph,
        sampler,
        scheduler,
        prompt,
        request
    ):
        # test_info = request.node.name
        # comfy_graph.set_filename_prefix(request)
        # Settings for comfy graph
        # comfy_graph.set_sampler_name(sampler)
        # comfy_graph.set_scheduler(scheduler)
        comfy_graph.set_prompt(prompt)

        # Generate
        output = client.get_videos(comfy_graph.graph)
        print(output.keys())

        assert len(output) != 0, "No images generated"
        # assert all images are not blank
        for images_output in output.values():
            print(type(images_output))
            for image_data in images_output:
                print(type(image_data))
                with open('video.mp4', 'wb') as file:
                    file.write(image_data)
                # pil_image = Image.open(BytesIO(image_data))
                # assert numpy.array(pil_image).any() != 0, "Image is blank"


if __name__ == "__main__":
    #
    # Initialize graphs
    #
    default_graph_file = 'dance_prompt.json'
    with open(default_graph_file, 'r') as file:
        default_graph = json.loads(file.read())

    DEFAULT_COMFY_GRAPH = ComfyGraph(graph=default_graph, input_nodes=['0'])
    DEFAULT_COMFY_GRAPH.set_prompt('a photo of a dark human')

    # DEFAULT_COMFY_GRAPH_ID = os.path.splitext(os.path.basename(default_graph_file))[0]
    # #
    # # Loop through these variables
    # #
    comfy_graph_list = [DEFAULT_COMFY_GRAPH]
    # comfy_graph_ids = [DEFAULT_COMFY_GRAPH_ID]
    # prompt_list = [
    #     'a photo of a dark human',
    # ]

    prompt_list = [
    'a photo of dark trees',]
    

    sampler_list = KSampler.SAMPLERS
    scheduler_list = KSampler.SCHEDULERS
    p = subprocess.Popen([
                'python', 'main.py',
                '--output-directory', 'tests/inference/output',
                '--listen', '127.0.0.1',
                '--port', '8188',
                ])
    test_i = TestInference()
    cg = ComfyGraph(graph=default_graph, input_nodes=['10','14'])
    comfy_client, comfy_graph = test_i._client_graph(cg)
    client = test_i.client(comfy_client)
    graph = test_i.comfy_graph(comfy_graph)

    TestInference().test_comfy(
        client=client, 
        comfy_graph=graph, 
        sampler=sampler_list[0], 
        scheduler=scheduler_list[0], 
        prompt=prompt_list[0], 
        request='pytestrequest'
    )
