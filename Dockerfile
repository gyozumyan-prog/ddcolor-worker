FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /app

RUN apt-get update && apt-get install -y git wget libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir runpod opencv-python-headless pillow requests huggingface_hub timm

# Clone DDColor and install
RUN git clone https://github.com/piddnad/DDColor.git /app/ddcolor
WORKDIR /app/ddcolor
RUN pip install -e .

# Download model
RUN mkdir -p /app/models && \
    wget -O /app/models/ddcolor_modelscope.pth https://huggingface.co/piddnad/ddcolor_modelscope/resolve/main/pytorch_model.pt

COPY rp_handler.py /app/
WORKDIR /app

CMD ["python", "-u", "rp_handler.py"]