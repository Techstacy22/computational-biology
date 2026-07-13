"""Logging setup for the CLI."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a logger configured with a simple 'LEVEL: message' format."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(handler)
    return logger


def set_verbosity(logger: logging.Logger, verbose: bool) -> None:
    """Set DEBUG level when --verbose is passed, WARNING otherwise."""
    logger.setLevel(logging.DEBUG if verbose else logging.WARNING)
