import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging(level=logging.INFO, log_file="fitness_tracker.log"):
    """Configure root logger for the application with file and console output."""
    fmt = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(fmt))
    root_logger.addHandler(console_handler)
    
    # File handler with rotation (max 5MB, keep 3 backup files)
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), log_file)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(fmt))
    root_logger.addHandler(file_handler)

    # Optionally adjust third-party loggers if noisy
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    return root_logger
