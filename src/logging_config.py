import logging


def configure_logging(level=logging.INFO):
    """Configure root logger for the application."""
    fmt = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
    logging.basicConfig(level=level, format=fmt)

    # Optionally adjust third-party loggers if noisy
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    return logging.getLogger()
