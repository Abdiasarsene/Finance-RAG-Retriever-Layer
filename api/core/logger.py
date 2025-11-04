# api/core/logger.py
from loguru import logger

logger.add("logs/retrieval_api.log", rotation="1 MB")