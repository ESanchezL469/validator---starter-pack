![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

# Validator - Starter Pack – Fase 1 (Validación y Versionado de Datasets)

Este proyecto permite cargar un dataset en CSV, validarlo automáticamente usando reglas definidas, generar un reporte de calidad, y versionarlo de forma reproducible.

## 📦 Estructura del Proyecto

```
dataops-starter-kit/
├── app/            # Lógica del proyecto (validación, reportería, almacenamiento)
├── datasets/       # Archivos validados y versionados
├── reports/        # Reportes de errores y calidad
├── metadata/       # Metadata del dataset validado
├── tests/          # Tests unitarios
├── Dockerfile      # (opcional)
├── requirements.txt
├── .gitignore
└── README.md
```

## ✅ Reglas de Validación
- `id`: entero positivo
- `name`: string
- `email`: formato válido de correo
- `age`: entre 18 y 99
- `created_at`: hora que fue creado
- `is_active`: booleano

## 🚀 Cómo usarlo

### Opción 1: Ejecutar localmente

1. Instala dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecuta el script:
```bash
python app/main.py
```

3. Ingresa la ruta de un CSV cuando lo solicite.

### Opción 2: Ejecutar con Docker

1. Construir la imagen:
```bash
docker build -t dataops-validator .
```

2. Ejecutar con volumen montado:
```bash
docker run -it -v $(pwd)/datasets:/app/datasets dataops-validator
```

> Asegúrate de montar también `reports/` y `metadata/` si quieres persistir esos archivos:
```bash
docker run -it \
  -v $(pwd)/datasets:/app/datasets \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/metadata:/app/metadata \
  dataops-validator
```

## 🧪 Tests

Para ejecutar tests:
```bash
pytest tests/
```

## 📌 Tecnologías usadas
- Python
- Pandas
- Pandera
- Pytest

## 🛠️ Uso con Makefile

También puedes ejecutar tareas comunes con `make`:

### Instalar dependencias
```bash
make install
```

### Ejecutar la app localmente
```bash
make run
```

### Ejecutar los tests
```bash
make test
```

### Construir imagen Docker
```bash
make docker-build
```

### Ejecutar contenedor Docker
```bash
make docker-run
```

---

## 🔧 Futuras mejoras
- Soporte para Excel
- Validaciones configurables por archivo
- Interfaz web con Streamlit
