from loguru import logger
from pathlib import Path

log_folder = Path("logs")
log_folder.mkdir(exist_ok=True)

logger.add(
    log_folder / "app.log",
    rotation="1 MB",     # rota al llegar a 1MB
    retention="7 days",  # guarda solo por 7 días
    compression="zip",   # comprime logs antiguos
    level="INFO"
)