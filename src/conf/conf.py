import logging.config


telegram_bot_token = ''


# Logging
# ----------------------------------------------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {'main': {'format': '%(levelname)s [%(asctime)s] %(message)s', 'datefmt': '%d/%m/%Y %H:%M:%S'}},
    'handlers': {'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'main'}},
    'loggers': {
        'telegram-smart-bot': {'handlers': ['console'], 'propagate': False, 'level': 'INFO'},
    }
}
logging.config.dictConfig(LOGGING)
