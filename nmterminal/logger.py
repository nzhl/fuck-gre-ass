from logging import getLogger, FileHandler, Formatter, DEBUG, WARNING
from os.path import isdir, join
from os import mkdir


from .config import DATA_PATH, LOG_PATH


def get_logger(name):
    if not isdir(DATA_PATH):
        mkdir(DATA_PATH)
    if not isdir(LOG_PATH):
        mkdir(LOG_PATH)

    logger = getLogger(name)
    logger.setLevel(DEBUG)
    logger.propagate = False # logs from child modules never pass to parent logger


    debug_handle = FileHandler(join(LOG_PATH, 'debug.log'))
    warning_handle = FileHandler(join(LOG_PATH, 'warning.log'))
    warning_handle.setLevel(WARNING)
    debug_handle.setFormatter(Formatter(
        '%(asctime)s - %(levelname)s - %(name)s:%(lineno)s: %(message)s')) 
    warning_handle.setFormatter(Formatter(
        '%(asctime)s - %(levelname)s - %(name)s:%(lineno)s: %(message)s')) 
    logger.addHandler(debug_handle)
    logger.addHandler(warning_handle)

    logger.debug(id(debug_handle))
    return logger
