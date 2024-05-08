from comfyui_graph.comfy_base_graph import ComfyGraph

class ComfyGraphText2img(ComfyGraph):

    def set_prompt(self, prompt, negative_prompt=None, **kwargs):
        for node in kwargs['text_prompt_nodes']:
            prompt_node = self.graph[node]['inputs']['positive'][0]
            self.graph[prompt_node]['inputs']['text'] = prompt
            if negative_prompt:
                negative_prompt_node = self.graph[node]['inputs']['negative'][0]
                self.graph[negative_prompt_node]['inputs']['text'] = negative_prompt


class ComfyGraphImg2img(ComfyGraph):
    def set_prompt(self, prompt, negative_prompt=None, **kwargs):
        for node in kwargs['text_prompt_nodes']:
            prompt_node = self.graph[node]['inputs']['positive'][0]
            self.graph[prompt_node]['inputs']['text'] = prompt
            if negative_prompt:
                negative_prompt_node = self.graph[node]['inputs']['negative'][0]
                self.graph[negative_prompt_node]['inputs']['text'] = negative_prompt
        for node in kwargs['image_prompt_nodes']:
            self.graph[node]['inputs']['image'] = kwargs['image_path']


class ComfyGraphText2video(ComfyGraph):
    def set_prompt(self, prompt, negative_prompt=None, **kwargs):
        for node in kwargs['text_prompt_nodes']:
            prompt_node = self.graph[node]['inputs']['positive'][0]
            self.graph[prompt_node]['inputs']['text'] = prompt
            if negative_prompt:
                negative_prompt_node = self.graph[node]['inputs']['negative'][0]
                self.graph[negative_prompt_node]['inputs']['text'] = negative_prompt