"""Test logging configuration."""

import pytest
import structlog
from logging_config import configure_logging


@pytest.fixture(autouse=True)
def reset_structlog():
    """Reset structlog before each test."""
    structlog.reset_defaults()
    yield
    structlog.reset_defaults()


def test_configure_logging_default():
    """Test default logging configuration (INFO level)."""
    configure_logging(verbose=False, quiet=False)

    logger = structlog.get_logger()
    logger.info("Test message")
    logger.debug("Debug message")


def test_configure_logging_verbose():
    """Test verbose logging configuration (DEBUG level)."""
    configure_logging(verbose=True, quiet=False)

    logger = structlog.get_logger()
    logger.info("Test message")
    logger.debug("Debug message")


def test_configure_logging_quiet():
    """Test quiet logging configuration (WARNING level)."""
    configure_logging(verbose=False, quiet=True)

    logger = structlog.get_logger()
    logger.info("Test message")
    logger.warning("Warning message")


def test_configure_logging_verbose_and_quiet():
    """Test that verbose takes precedence when both flags are set."""
    configure_logging(verbose=True, quiet=True)

    logger = structlog.get_logger()
    logger.debug("Debug message")
