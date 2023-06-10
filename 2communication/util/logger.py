import logging

logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s')

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

