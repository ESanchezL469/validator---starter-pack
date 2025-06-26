# Validator - Starter Pack – Fase 2 (Validación, Enriquecimiento y Metadata)

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
