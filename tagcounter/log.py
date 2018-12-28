import logging
import sys

from pkg_resources import resource_filename

import resources

CONSOLE_FORMATTER = logging.Formatter('%(name)s:%(lineno)d:%(levelname)s:%(message)s')
PERSISTENT_FORMATTER = logging.Formatter('%(asctime)s:%(message)s')

LEVEL = logging.DEBUG


def get_console_handler() -> logging.Handler:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CONSOLE_FORMATTER)
    return console_handler


def get_file_handler(file_name: str = resource_filename('resources', resources.LOG_FILE)) -> logging.Handler:
    handler = logging.FileHandler(file_name)
    handler.setLevel(LEVEL)
    handler.setFormatter(PERSISTENT_FORMATTER)

    return handler


def _create_logger(name: str, handler: logging.Handler) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LEVEL)
    logger.addHandler(handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    return _create_logger(name, get_console_handler())


def get_persistent_logger(name: str) -> logging.Logger:
    return _create_logger(name, get_file_handler())


