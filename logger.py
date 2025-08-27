import os
from loguru import logger
import sys

env = os.getenv("ENV", "dev")

if env == "dev":
    logger.add(sys.stderr, level="DEBUG")
else:
    logger.add("logs/api.log", rotation="1 MB", retention="10 days", compression="zip", level="INFO")
