import logging
from config import config

def setup_logger() -> None:
    config.ensure_directories()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config.LOG_DIR / "app.log"),
        ]
    )

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)