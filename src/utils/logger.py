import logging.handlers

from conf import LOGGING_LEVEL

formatter = logging.Formatter(fmt='%(levelname)s [%(asctime)s] %(message)s',
                              datefmt='%d/%m/%Y %H:%M:%S')

# logging.basicConfig(level=logging.WARNING,
#                     format='%(levelname)s [%(asctime)s] %(message)s',
#                     datefmt='%d/%m/%Y %H:%M:%S')

handlers = [logging.StreamHandler()]


try:
    fl = logging.handlers.RotatingFileHandler('./log/logs.log', encoding='utf8', maxBytes=100000000, backupCount=1)
except FileNotFoundError:
    print('NO LOG FILE')
else:
    handlers.append(fl)


for handler in handlers:
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)


def get_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(LOGGING_LEVEL)

    logger = logging.getLogger(__name__)

    for handl in handlers:
        logger.addHandler(handl)

    return logger
