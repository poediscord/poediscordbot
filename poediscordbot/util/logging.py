import logging
import sys

import logging.config
from instance import config


def init_logging():
    logging_conf = {
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
                'filename': config.ROOT_DIR + '/discord_pob.logger',
                'mode': 'w',
                'class': 'logging.FileHandler',
            }
        },
        'loggers': {
            'discord_pob': {'level': 'INFO',
                   'handlers': ['console', 'file'],
                   'propagate': False},
            'discord': {'level': 'INFO'},
            'discord.http': {'level': 'INFO'}
        }
    }

    logging.config.dictConfig(logging_conf)
    logger = logging.getLogger('discord_pob')
    logger.setLevel(config.debug_level)
    return logger


log = init_logging()
