import runpod
import base64
import tempfile
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

print("Loading DDColor model...")
colorizer = ImageColorizationPipeline(
    model_path='/app/models/ddcolor_modelscope.pth',
    input_size=512
)
print("DDColor loaded!")

def handler(event):
    try:
        inp = event.get('input', {})
        img_data = inp.get('image')
        input_type = inp.get('input_type', 'base64')
        
        # Load image
        if input_type == 'url':
            r = requests.get(img_data, timeout=60)
            img = Image.open(BytesIO(r.content)).convert('RGB')
        else:
            img_bytes = base64.b64decode(img_data)
            img = Image.open(BytesIO(img_bytes)).convert('RGB')
        
        # Convert to numpy
        img_np = np.array(img)
        
        # Colorize
        result = colorizer.process(img_np)
        
        # Encode result
        _, buf = cv2.imencode('.png', cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
        b64 = base64.b64encode(buf).decode('utf-8')
        
        return {"image": b64}
    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}

runpod.serverless.start({"handler": handler})