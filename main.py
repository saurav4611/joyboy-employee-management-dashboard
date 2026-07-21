import sys
from PySide6.QtWidgets import QApplication

from config import config
from utils.logger import setup_logger, get_logger
from database.session import DatabaseManager
from database.seed import seed_database
from ui.main_window import MainWindow
from ui.styles import STYLESHEET

def main() -> None:
    config.ensure_directories()
    setup_logger()
    logger = get_logger("main")
    logger.info("Starting %s v%s", config.APP_NAME, config.APP_VERSION)

    # Initialize database and seed data
    DatabaseManager.initialize()
    seed_database()

    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)
    app.setStyleSheet(STYLESHEET)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()