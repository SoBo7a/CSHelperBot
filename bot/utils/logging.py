import logging
from typing import Optional


def get_log_level(level: str) -> int:
    """
    Convert a string log level to its corresponding integer value.

    Args:
        level (str): The string representation of the log level.

    Returns:
        int: The integer value of the log level.
    """
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    return levels.get(level.upper(), logging.DEBUG)


def get_cs_butler_logger(log_level: Optional[str] = "DEBUG") -> logging.Logger:
    """
    Retrieve a logger instance for the CS Butler bot.

    Args:
        log_level (Optional[str]): The string representation of the log level.
            Valid options are: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL".
            Defaults to "DEBUG".

    Returns:
        logging.Logger: A logger instance configured for the CS Butler bot.
    """
    numeric_level = get_log_level(log_level)
    logger = logging.getLogger('discord.cs_butler')
    logger.setLevel(numeric_level)
    
    return logger
