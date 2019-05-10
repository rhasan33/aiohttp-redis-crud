import os
import logging
import logging.config


def search_logger(name):
    dict_logger = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '[%(asctime)s][%(levelname)s] %(name)s'
                          '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
                'datefmt': '%H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'console'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'search': {
                'level': 'INFO',
                'propagate': True,
            }
        }
    }
    logging.config.dictConfig(dict_logger)
    return logging.getLogger(name)
