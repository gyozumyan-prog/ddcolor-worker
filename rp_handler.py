import runpod
import base64
import tempfile
import os
import cv2
import requests

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
from PIL import Image
from io import BytesIO

# Инициализация пайплайна (грузится из кэша /app/models)
colorizer = pipeline(
    task=Tasks.image_colorization,
    model='damo/cv_ddcolor_image-colorization',
    model_dir='/app/models'
)

def handler(event):
    inp = event.get("input", {})
    img_data = inp.get("image")
    input_type = inp.get("input_type", "base64")

    if not img_data:
        return {"error": "No image provided"}

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        if input_type == "url":
            r = requests.get(img_data, timeout=30)
            r.raise_for_status()
            Image.open(BytesIO(r.content)).convert("RGB").save(tmp.name)
        else:
            tmp.write(base64.b64decode(img_data))

        result = colorizer(tmp.name)
        img = result[OutputKeys.OUTPUT_IMG]

        _, buf = cv2.imencode(".png", img)

    os.unlink(tmp.name)

    return {
        "image": base64.b64encode(buf).decode("utf-8")
    }

runpod.serverless.start({"handler": handler})
