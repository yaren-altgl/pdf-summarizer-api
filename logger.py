# logger.py
from loguru import logger

# Log dosyasına yazmak istersen:
logger.add("logs/api.log", rotation="1 MB", retention="10 days", compression="zip")

# İstersen sadece terminale yazsın:
# logger.add(sys.stderr, level="INFO")
