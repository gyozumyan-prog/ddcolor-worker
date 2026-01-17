import runpod
import base64
import tempfile
import os
import cv2
import requests
from PIL import Image
from io import BytesIO
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

print("Loading DDColor model...")
colorizer = pipeline(Tasks.image_colorization, model='damo/cv_ddcolor_image-colorization')
print("DDColor model loaded!")

def handler(event):
    try:
        inp = event.get('input', {})
        img_data = inp.get('image')
        input_type = inp.get('input_type', 'base64')
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            if input_type == 'url':
                r = requests.get(img_data, timeout=60)
                img = Image.open(BytesIO(r.content)).convert('RGB')
                img.save(tmp.name)
            else:
                img_bytes = base64.b64decode(img_data)
                with open(tmp.name, 'wb') as f:
                    f.write(img_bytes)
            
            result = colorizer(tmp.name)
            colorized = result[OutputKeys.OUTPUT_IMG]
            
            # Convert BGR to RGB
            colorized_rgb = cv2.cvtColor(colorized, cv2.COLOR_BGR2RGB)
            _, buf = cv2.imencode('.png', colorized_rgb)
            
            os.unlink(tmp.name)
            return {"image": base64.b64encode(buf).decode('utf-8')}
    except Exception as e:
        return {"error": str(e)}

runpod.serverless.start({"handler": handler})