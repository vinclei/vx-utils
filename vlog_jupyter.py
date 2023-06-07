import logging
# import os
import sys
from logging import Formatter


class Color(object):
    """
    utility to return ansi colored text.
    """

    colors = {
        "black": 30,
        "red": 31,
        "green": 92,
        "yellow": 93,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "grey": 90,
        "bgred": 41,
        "bggrey": 100,
    }

    prefix = "\033["

    suffix = "\033[0m"

    def colored(self, text, color=None):
        if color not in self.colors:
            color = "white"

        clr = self.colors[color]
        return (self.prefix + "%dm%s" + self.suffix) % (clr, text)


colored = Color().colored


class ColoredFormatter(Formatter):
    def format(self, record):
        # message = record.getMessage()

        mapping = {
            "INFO": "blue",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bgred",
            "DEBUG": "grey",
            "SUCCESS": "green",
        }

        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        clr = mapping.get(record.levelname, "white")
        log_fmt = colored(format, clr)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# globalLogger = None

# if "LOG_LEVEL" in os.environ and hasattr(logging, os.environ["LOG_LEVEL"]):
#     LOG_LEVEL = getattr(logging, os.environ["LOG_LEVEL"])
# else:
#     LOG_LEVEL = logging.INFO


def get_logger(name, file=None, log_level="DEBUG"):
    # global globalLogger
    # if globalLogger is not None:
    #     return globalLogger

    # Create a custom logger
    logger = logging.getLogger(name)
    logging.basicConfig()
    logger.propagate = False

    # Check if handlers exist
    handlers = logging.getLogger().handlers
    for h in handlers:
        if isinstance(h, logging.StreamHandler):
            c_handler = h
            break

    # Create handlers
    if c_handler is None:
        c_handler = logging.StreamHandler(sys.stderr)
        c_handler.setFormatter(ColoredFormatter())

    # Create formatters and add it to handlers
    # c_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # set success level
    logging.SUCCESS = 25  # between WARNING and INFO
    logging.addLevelName(logging.SUCCESS, "SUCCESS")
    setattr(logger, "success", lambda message, *args: logger._log(logging.SUCCESS, message, args))

    # Add handlers to the logger
    logger.addHandler(c_handler)

    if file is not None:
        f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)")
        f_handler = logging.FileHandler(file)
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

    if log_level is None:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(log_level)

    # globalLogger = logger
    return logger


def get_logger_simple(log_level=logging.DEBUG):
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger()
    logger.propagate = False
    return logger