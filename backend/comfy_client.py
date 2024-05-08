import websocket
import uuid
import urllib.request
import urllib.parse
import random
import json
from utils.qiniu_oss import QINIU_OBJ


class ComfyClient:
    def __init__(self,
                 input_dir='',
                 output_dir='',
                 listen='127.0.0.1',
                 port=8188,
                 client_id=str(uuid.uuid4()),
                 ):
        self.client_id = client_id
        self.server_address = f"{listen}:{port}"
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.server_address, self.client_id))
        self.ws = ws
        self.input_dir = input_dir
        self.output_dir = output_dir

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request("http://{}/prompt".format(self.server_address), data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}".format(self.server_address, url_values)) as response:
            return response.read()

    def get_history(self, prompt_id):
        with urllib.request.urlopen("http://{}/history/{}".format(self.server_address, prompt_id)) as response:
            return json.loads(response.read())

    def get_output(self, graph, save=True):
        prompt = graph
        if not save:
            # Replace save nodes with preview nodes
            prompt_str = json.dumps(prompt)
            prompt_str = prompt_str.replace('SaveImage', 'PreviewImage')
            prompt = json.loads(prompt_str)

        prompt_id = self.queue_prompt(prompt)['prompt_id']
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break  # Execution is done
            else:
                continue  # previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        return history

    def get_images(self, graph, save=True):
        prompt = graph
        if not save:
            # Replace save nodes with preview nodes
            prompt_str = json.dumps(prompt)
            prompt_str = prompt_str.replace('SaveImage', 'PreviewImage')
            prompt = json.loads(prompt_str)

        prompt_id = self.queue_prompt(prompt)['prompt_id']
        output_images = {}
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break  # Execution is done
            else:
                continue  # previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        images_output = []
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    file_name = image['filename']
                    file_path = '{}/{}'.format(self.output_dir, file_name)
                    images_output.append(QINIU_OBJ.fput_file('metaagent', file_path, 'DrawImage_PSD'))

        return images_output

    def get_video_webp(self, graph, save=True):
        prompt = graph
        if not save:
            # Replace save nodes with preview nodes
            prompt_str = json.dumps(prompt)
            prompt_str = prompt_str.replace('SaveImage', 'PreviewImage')
            prompt = json.loads(prompt_str)
        prompt_id = self.queue_prompt(prompt)['prompt_id']
        output_video = []
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break  # Execution is done
            else:
                continue  # previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output and '.webp' in node_output['images'][0]['filename']:
                for image in node_output['images']:
                    file_name = image['filename']
                    file_path = '{}/{}'.format(self.output_dir, file_name)
                    output_video.append(QINIU_OBJ.fput_file('metaagent', file_path, 'DrawImage_PSD'))
        return output_video
