import runpod
import base64
import os
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import requests
import torch
import sys

sys.path.insert(0, '/app/ddcolor')
from inference.colorization_pipeline import ImageColorizationPipeline

print("Loading DDColor...")
colorizer = ImageColorizationPipeline(
    model_path='/app/models/ddcolor_paper.pth',
    input_size=512
)
print("DDColor ready!")

def handler(event):
    try:
        inp = event.get('input', {})
        img_data = inp.get('image')
        input_type = inp.get('input_type', 'base64')
        
        if input_type == 'url':
            r = requests.get(img_data, timeout=60)
            img = Image.open(BytesIO(r.content)).convert('RGB')
        else:
            img = Image.open(BytesIO(base64.b64decode(img_data))).convert('RGB')
        
        result = colorizer.process(np.array(img))
        _, buf = cv2.imencode('.png', cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
        
        return {"image": base64.b64encode(buf).decode('utf-8')}
    except Exception as e:
        return {"error": str(e)}

runpod.serverless.start({"handler": handler})