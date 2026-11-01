from pathlib import Path
import sys

from loguru import logger

from app.utils.config import settings


# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Remove default logger
logger.remove()

# Console Logger
logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    ),
)

# File Logger
logger.add(
    LOG_DIR / "app.log",
    level=settings.LOG_LEVEL,
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)

# Error Logger
logger.add(
    LOG_DIR / "error.log",
    level="ERROR",
    rotation="5 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)


def get_logger():
    """
    Returns the configured Loguru logger.

    Usage:
        from app.utils.logger import get_logger

        logger = get_logger()
        logger.info("Application started")
    """
    return logger