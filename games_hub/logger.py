import logging

from games_hub.static import *


def _get_logger():
    temp_logger = logging.getLogger()
    temp_logger.setLevel(logging.DEBUG)

    # file Log
    f_handler = logging.FileHandler("log.txt", encoding='utf-8')
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(LOG_FORMAT)

    # console Log
    s_handler = logging.StreamHandler()
    s_handler.setLevel(logging.INFO)
    s_handler.setFormatter(LOG_FORMAT_WITHOUT_LEVEL_NAME)

    # add handler to logger
    temp_logger.addHandler(f_handler)
    temp_logger.addHandler(s_handler)
    temp_logger.name = PROJECT_NAME
    return temp_logger


logger = _get_logger()
