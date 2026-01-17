FROM runpod/base:0.6.2-cuda12.1.0

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt


RUN python3 -c "from modelscope.hub.snapshot_download import snapshot_download; snapshot_download('damo/cv_ddcolor_image-colorization', cache_dir='/app/models')"

COPY rp_handler.py .

CMD ["python3", "-u", "rp_handler.py"]
