FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget libgl1 libglib2.0-0 tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir runpod opencv-python-headless pillow requests huggingface_hub timm basicsr

# Clone DDColor
RUN git clone https://github.com/piddnad/DDColor.git /app/ddcolor
WORKDIR /app/ddcolor
RUN pip install --no-cache-dir -r requirements.txt

# Download model
RUN mkdir -p /app/models && \
    python -c "from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='piddnad/ddcolor_paper', filename='ddcolor_paper.pth', local_dir='/app/models')"

COPY rp_handler.py /app/
WORKDIR /app

CMD ["python", "-u", "rp_handler.py"]