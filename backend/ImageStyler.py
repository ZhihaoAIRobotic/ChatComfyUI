import torch
from safetensors.torch import load_file
from diffusers import StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler
from diffusers import DiffusionPipeline
import torch
from safetensors.torch import load_file
from diffusers import StableDiffusionXLPipeline

class ImageStyler:
    def __init__(self, model_path, lora_model_path):
        self.base = None
        self.pipeline = None
        self.lora_model_path = lora_model_path
        self.model_path = model_path

    def load_models(self):
        self.base = StableDiffusionXLPipeline.from_single_file(
            self.model_path,
            torch_dtype=torch.float16,
            original_config_file='./sd_xl_base.yaml',
            use_safetensors=True,
            safety_checker=None
        ).to("cuda")


        self.base.load_lora_weights(self.lora_model_path)

        # Load additional models here if needed

    def style_image(self, prompt, negative_prompt, generator):
        with torch.no_grad():
            image = self.base(
                prompt=prompt,
                num_inference_steps=50,
                guidance_scale=15,
                negative_prompt=negative_prompt,
                generator=torch.manual_seed(generator)
            ).images[0]

        return image
