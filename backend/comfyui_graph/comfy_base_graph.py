from abc import ABC, abstractmethod

class ComfyGraph(ABC):
    def __init__(self,
                 graph
                 ):
        self.graph = graph

    @abstractmethod
    def set_prompt(self, prompt, negative_prompt=None, **kwargs):
        pass