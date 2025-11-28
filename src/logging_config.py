import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging(level=logging.INFO, log_dir=None, logfile_name="fitness_tracker.log"):
    """Configure root logger with console and rotating file handlers.

    - level: logging level (default INFO)
    - log_dir: directory to store log files (defaults to project root `logs/`)
    Returns the root logger.
    """
    fmt = "%(asctime)s.%(msecs)03d %(levelname)-7s %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    root = logging.getLogger()
    # avoid adding handlers multiple times if configure_logging is called more than once
    if root.handlers:
        for h in list(root.handlers):
            root.removeHandler(h)

    root.setLevel(level)

    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
    root.addHandler(console)

    # File logger
    if log_dir is None:
        # default to a `logs/` folder next to the project root
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        log_dir = os.path.join(base, "logs")
    os.makedirs(log_dir, exist_ok=True)
    logfile = os.path.join(log_dir, logfile_name)
    file_handler = RotatingFileHandler(logfile, maxBytes=1024 * 1024, backupCount=3, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
    root.addHandler(file_handler)

    # Tame noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    return root


def get_logger(name=None):
    """Convenience wrapper to get a module logger after configuration."""
    return logging.getLogger(name)
