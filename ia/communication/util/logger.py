import logging
from communication.util.logger_formatter import CustomFormatter

logger_level = logging.INFO # Change to logging.DEBUG to see debug messages

""" DO NOT MODIFY THIS UNDER THIS LINE """
logger = logging.getLogger('logger')
if len(logger.handlers) == 0:
    logger.setLevel(logger_level)
    sh = logging.StreamHandler()
    sh.setLevel(logger_level)
    sh.setFormatter(CustomFormatter())
    logger.addHandler(sh)
