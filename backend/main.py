from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/text2img/")
def text2img(prompt,negative_prompt):
    print(prompt)
    print(negative_prompt)
    import uuid
    from ImageStyler import ImageStyler
    from PIL import Image
    from qiniu_oss import QINIU_OBJ
    model_path = './sdXL_v10.safetensors'
    lora_model_path = './Ath_stuffed-toy_XL.safetensors'
    styler = ImageStyler(model_path, lora_model_path)
    styler.load_models()
    styled_image = styler.style_image(prompt, negative_prompt, generator=2960)
    styled_image_name = str(uuid.uuid4()) + ".jpg"
    styled_image.save(styled_image_name)
    url = QINIU_OBJ.fput_file('metaagent', styled_image_name, 'DrawImage_PSD')
    return {"url": url}