import logging
from logging import Logger

FORMAT = (
    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] " "- %(message)s"
)


def init_logger(name: str) -> Logger:
    logging.basicConfig(filename="backend.log", filemode="a", format=FORMAT)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
