# 📓 Changelog - Validator - Starter Pack

Todas las versiones y cambios documentados siguiendo [Keep a Changelog](https://keepachangelog.com/) y [Semantic Versioning](https://semver.org/lang/es/).

---

## [0.3.0] - 2025-06-25
### Añadido
- Procesamiento de múltiples archivos vía `--input` y `--input-folder`.
- Soporte para archivos `.csv` y `.xlsx`.
- Detección de versiones anteriores (`replaces`) para seguimiento.
- Validación contra duplicados mediante hashing del dataset.
- Modularización completa (ingestor, tracker, enricher, metadata_writer).
- Test de integración end-to-end (`test_pipeline_input_folder.py`).
- Soporte inicial de `argparse`.

---

## [0.2.0] - 2025-06-18
### Añadido
- Enriquecimiento de datos (`age_group`, `signup_year`).
- Generación automática de metadatos (`version`, `timestamp`, `source_file`).
- Carpeta `metadata/` y escritor de metadatos estructurado (`metadata_writer.py`).

---

## [0.1.0] - 2025-06-11
### Añadido
- Validación de estructura y tipos con `Pandera`.
- Registro de errores de validación en archivos `.txt`.
- Almacenamiento de datasets validados en `datasets/` usando hash.
- Estructura básica de carpetas y ejecución simple con `main.py`.
- Dockerfile base y configuración inicial de `Makefile`.

---
