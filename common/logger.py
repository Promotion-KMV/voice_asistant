import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setFormatter(logging.Formatter("%(asctime)s [ %(levelname)s ] %(message)s"))
stdout_handler.setLevel(logging.DEBUG)

logger.addHandler(stdout_handler)
