import os

EMAIL = os.getenv('EMAIL') or 'bot@dogood.com'
PASSWORD = os.getenv('PASSWORD') or 'secret'


LOGGING_CONFIG = 'logging.config.dictConfig'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(name)s %(module)s %(process)d %(thread)d  %(message)s'
        },
        'timestamped': {
            'format': '%(asctime)s %(levelname)s %(name)s  %(message)s'
        },
        'simple': {
            'format': '%(levelname)s  %(message)s'
        },
        'performance': {
            'format': '%(asctime)s %(process)d | %(thread)d | %(message)s',
        },
    },
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'timestamped',
        },
    },
    'loggers': {
        'bot': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}

PLUGINS = {
    'daisie': {
        'subreddit': 'https://www.reddit.com/r/DaisyRidley/',
    },
}
