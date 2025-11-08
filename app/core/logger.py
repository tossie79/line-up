import logging

# Simple logger that replaces print statements
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger("lineup_api")
