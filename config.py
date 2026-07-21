import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    APP_NAME: str = os.getenv("APP_NAME", "JoyBoy Flow")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    
    DATABASE_DIR: Path = BASE_DIR / "database"
    _default_db_path: Path = DATABASE_DIR / "joyboy_flow.db"
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{_default_db_path.as_posix()}")
    
    LOG_DIR: Path = BASE_DIR / os.getenv("LOG_DIR", "logs")
    EXPORT_DIR: Path = BASE_DIR / os.getenv("EXPORT_DIR", "exports")
    ASSETS_DIR: Path = BASE_DIR / os.getenv("ASSETS_DIR", "assets")

    @classmethod
    def ensure_directories(cls) -> None:
        for directory in [cls.DATABASE_DIR, cls.LOG_DIR, cls.EXPORT_DIR, cls.ASSETS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

config = Config()