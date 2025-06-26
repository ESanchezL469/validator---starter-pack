FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

WORKDIR /app

# Instalar solo lo necesario y limpiar cache
RUN apt-get update && apt-get install -y gcc && \
    pip install --upgrade pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY datasets/ datasets/
COPY reports/ reports/
COPY metadata/ metadata/

CMD ["python", "app/main.py"]