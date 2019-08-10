import logging
import logging.config
import sys

from instance import config


def init_logging(name):
    DEFAULT_LOGGING = {
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                'datefmt': '%Y-%m-%d - %H:%M:%S'},
        },
        'handlers': {
            'console': {'class': 'logging.StreamHandler',
                        'formatter': "standard",
                        'level': config.debug_level,
                        'stream': sys.stdout
                        },
            'file': {
                'formatter': "standard",
                'level': config.debug_level,
                'filename': config.ROOT_DIR + '/discord_pob.log',
                'mode': 'w',
                'class': 'logging.FileHandler',
            }
        },
        'loggers': {
            name: {'level': 'INFO',
                   'handlers': ['console', 'file'],
                   'propagate': False},
        }
    }

    logging.config.dictConfig(DEFAULT_LOGGING)
    log = logging.getLogger(name)
    log.setLevel(config.debug_level)
    return log


# print(config.ROOT_DIR)
log = init_logging("discord_pob")
