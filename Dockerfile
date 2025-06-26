# Imagen base
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias y código
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY datasets/ datasets/
COPY reports/ reports/
COPY metadata/ metadata/

# Comando por defecto
CMD ["python", "app/main.py"]
