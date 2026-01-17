FROM runpod/base:0.6.2-cuda12.1.0

WORKDIR /app

# Системные зависимости для opencv / PIL
RUN apt-get update && apt-get install -y \
    git \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements
COPY requirements.txt .

# КРИТИЧНО: обновляем pip и ставим только бинарники
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# Предскачиваем модель (чтобы не было cold download)
RUN python3 - <<'EOF'
from modelscope.hub.snapshot_download import snapshot_download
snapshot_download(
    'damo/cv_ddcolor_image-colorization',
    cache_dir='/app/models'
)
EOF

# Копируем handler
COPY rp_handler.py .

CMD ["python3", "-u", "rp_handler.py"]
