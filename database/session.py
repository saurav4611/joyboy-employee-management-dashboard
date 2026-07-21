from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from config import config
from database.base import Base
from models.employee import Employee  # Required for metadata registration
from models.attendance import Attendance  # Required for metadata registration
from utils.logger import get_logger

logger = get_logger("database.session")

class DatabaseManager:
    _engine = None
    _session_factory = None

    @classmethod
    def initialize(cls) -> None:
        if cls._engine is not None:
            return
        
        config.ensure_directories()
        logger.info("Initializing database engine: %s", config.DATABASE_URL)
        cls._engine = create_engine(config.DATABASE_URL, echo=False, future=True)
        
        @event.listens_for(cls._engine, "connect")
        def _set_sqlite_pragma(dbapi_conn, _):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.close()

        cls._session_factory = sessionmaker(bind=cls._engine, expire_on_commit=False, future=True)
        
        # Create tables if they don't exist
        Base.metadata.create_all(cls._engine)
        logger.info("Database initialized and tables verified.")

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls.initialize()
        return cls._engine

    @classmethod
    def get_session(cls) -> Session:
        if cls._session_factory is None:
            cls.initialize()
        return cls._session_factory()

    @classmethod
    def dispose(cls) -> None:
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None
            logger.info("Database engine disposed.")