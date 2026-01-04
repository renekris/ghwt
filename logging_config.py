"""Structured logging configuration for CLI tools."""

import structlog


def configure_logging(
    verbose: bool = False,
    quiet: bool = False,
) -> None:
    """Configure structlog for CLI tools.

    Args:
        verbose: Enable DEBUG level logging
        quiet: Suppress INFO level, show only WARNING/ERROR
    """
    # Determine log level
    if quiet:
        level = "WARNING"
    elif verbose:
        level = "DEBUG"
    else:
        level = "INFO"

    # Configure structlog for console output
    structlog.configure(
        processors=[
            # Add log level
            structlog.stdlib.add_log_level,
            # Add timestamp
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            # Format exceptions
            structlog.processors.format_exc_info,
            # Pretty console output
            structlog.dev.ConsoleRenderer(colors=True),
        ],
        # Set log level
        wrapper_class=structlog.make_filtering_bound_logger(level),
        # Use print-based logger (no files for CLI tools)
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
