import logging


def setup_logging(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("visionops")
    logger.setLevel(level.upper())

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)

    logger.propagate = False
    return logger


logger = setup_logging()
