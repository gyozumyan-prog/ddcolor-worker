import runpod, base64, tempfile, os, cv2, requests
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
from PIL import Image
from io import BytesIO

colorizer = pipeline(Tasks.image_colorization, model='damo/cv_ddcolor_image-colorization')

def handler(event):
    inp = event.get('input', {})
    img_data = inp.get('image')
    input_type = inp.get('input_type', 'base64')
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        if input_type == 'url':
            r = requests.get(img_data, timeout=30)
            Image.open(BytesIO(r.content)).save(tmp.name)
        else:
            tmp.write(base64.b64decode(img_data))
        
        result = colorizer(tmp.name)
        img = result[OutputKeys.OUTPUT_IMG]
        _, buf = cv2.imencode('.png', img)
        os.unlink(tmp.name)
        return {"image": base64.b64encode(buf).decode('utf-8')}

runpod.serverless.start({"handler": handler})