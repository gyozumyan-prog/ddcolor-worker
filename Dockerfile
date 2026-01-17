FROM runpod/base:0.6.2-cuda12.1.0
WORKDIR /app

RUN apt-get update && apt-get install -y \
    git libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rp_handler.py .
CMD ["python3", "-u", "rp_handler.py"]