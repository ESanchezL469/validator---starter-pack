# Validator - Starter Pack

![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Este proyecto permite cargar un dataset en CSV, validarlo automáticamente usando reglas definidas, generar un reporte de calidad, y versionarlo de forma reproducible.

## 📥 Clonar el proyecto

Clona el repositorio y entra al directorio:

```bash
git clone https://github.com/tu_usuario/validator---starter-pack.git
cd validator---starter-pack.git
```

## 📦 Estructura del Proyecto

```
.
├── app/
│   ├── main.py
│   ├── validator.py
│   ├── enricher.py
│   ├── reporter.py
│   ├── metadata_writer.py
│   ├── storage.py
│   ├── ingestor.py
│   ├── source_tracker.py
│   └── profiler.py
├── datasets/
├── reports/
├── metadata/
├── profiles/
├── tests/
│   ├── test_pipeline_input_file.py
│   └── test_pipeline_input_folder.py
├── .env
├── .gitignore
├── requirements.txt
├── Dockerfile
├── Makefile
└── README.md
```

## ✅ Reglas de Validación
- `id`: entero positivo
- `name`: string
- `email`: formato válido de correo
- `age`: entre 18 y 99
- `created_at`: hora que fue creado
- `is_active`: booleano

### 🧠 Enriquecimiento automático

Al cargar un archivo, el sistema agrega automáticamente:

- `age_group`: clasificación en joven, adulto o senior
- `signup_year`: año de registro a partir de `created_at`

### 📄 Reporte automático

Se genera un archivo `.txt` con:

- Errores por columna
- Reglas fallidas
- Estadísticas básicas (`describe()`) si los datos son válidos

### 📊 Metadata estructurada

Para cada archivo procesado se crea un `.json` con:

- Versión (hash del contenido)
- Timestamp
- Columnas presentes
- Resultado de validación
- Total de filas

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

> Asegúrate de montar también `reports/`, `metadata/` y `profiles/` si quieres persistir los resultados.
```bash
docker run -it \
  -v $(pwd)/datasets:/app/datasets \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/metadata:/app/metadata \
  -v $(pwd)/metadata:/app/profiles \
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
- ydata-profiling
- Pytest
- setuptools

## 🛠️ Uso con Makefile

Tareas comunes:

```bash
make install        # Instala dependencias
make run            # Ejecuta el validador
make test           # Corre pruebas
make docker-build   # Construye imagen Docker
make docker-run     # Ejecuta el contenedor
```

## 🗂️ Archivos generados
- `datasets/`: archivos validados con nombre `{hash}_data.csv`
- `reports/`: reportes de calidad `{hash}_report.txt`
- `metadata/`: metadatos `{hash}_metadata.json`
- `profiles/`: perfil exploratorio `{hash}_profile.html`

---

## 🔮 Próximas fases

- Integrar `great_expectations` como capa de validación extendida
- Soporte para almacenamiento en S3 o GCS
- Logging estructurado
- Orquestación con Airflow o Dagster