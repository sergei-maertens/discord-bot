import os
from urllib.parse import urljoin

PROJECT_ROOT = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

DEBUG = bool(os.getenv('DEBUG', 0))

TOKEN = os.getenv('TOKEN') or 'my-discord-token'
EMAIL = os.getenv('EMAIL') or 'bot@dogood.com'
PASSWORD = os.getenv('PASSWORD') or 'secret'
OWNER_ID = os.getenv('OWNER_ID')

SECRET_KEY = os.getenv('SECRET_KEY', 'i-am-very-secret')

SITE_URL = 'https://botbt.xbbtx.be'
GITHUB_URL = 'https://github.com/sergei-maertens/discord-bot'

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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bot.accounts',
    'bot.channels',
    'bot.games',
    'bot.users',

    'bot.plugins.custom_commands',
    'bot.plugins.game_notifications',
    'bot.plugins.reddit',
    'bot.plugins.remindme',
    'bot.plugins.stats',
    'bot.plugins.status',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'bot', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


PRAW_USER_AGENT = 'python:discord-fetcher:v0.0.1 (by /u/xBBTx)'


PLUGINS = {
    'log': {
        'enabled': True,
    },
    'custom_commands': {
        'enabled': True,
    },
    'game_notifications': {
        'enabled': True,
    },
    'help': {
        'enabled': True,
    },
    'test': {
        'enabled': True,
    },
    'system': {
        'enabled': True,
    },
    'random_commands': {
        'enabled': True,
    },
    'reddit': {
        'enabled': True,
        'useragent': PRAW_USER_AGENT,
    },
    'stats': {
        'enabled': True,
    },
    'status': {
        'enabled': True,
    },
    'refuse_command': {
        'enabled': True,
    },
    'remindme': {
        'enabled': True,
    }
}


USE_TZ = True
TIME_ZONE = 'Europe/Amsterdam'

ROOT_URLCONF = 'bot.urls'

AUTH_USER_MODEL = 'accounts.User'


STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = urljoin(SITE_URL, '/media/')


ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'botbt.xbbtx.be']


WSGI_APPLICATION = 'bot.wsgi.application'


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
