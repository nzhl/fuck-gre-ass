from logging import getLogger, FileHandler, Formatter, DEBUG, WARNING
from os.path import isdir, join
from os import mkdir


from .config import *


def get_logger(name):
    if not isdir(DATA_DIR):
        mkdir(DATA_DIR)
    if not isdir(LOG_DIR):
        mkdir(LOG_DIR)

    logger = getLogger(name)
    logger.setLevel(DEBUG)
    logger.propagate = False # logs from child modules never pass to parent logger


    debug_handle = FileHandler(join(LOG_DIR, 'debug.log'))
    warning_handle = FileHandler(join(LOG_DIR, 'warning.log'))
    warning_handle.setLevel(WARNING)
    debug_handle.setFormatter(Formatter(
        '%(asctime)s - %(levelname)s - %(name)s:%(lineno)s: %(message)s')) 
    warning_handle.setFormatter(Formatter(
        '%(asctime)s - %(levelname)s - %(name)s:%(lineno)s: %(message)s')) 
    logger.addHandler(debug_handle)
    logger.addHandler(warning_handle)

    return logger
