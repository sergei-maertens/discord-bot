import logging
import sys
from importlib import import_module


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'bot': {
            'handlers': ['console'],
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        raise ImportError(msg)

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
            dotted_path, class_name)
        raise ImportError(msg)


def configure_logging(logging_config, logging_settings):
    if not sys.warnoptions:
        # Route warnings through python logging
        logging.captureWarnings(True)

    if logging_config:
        # First find the logging configuration function ...
        logging_config_func = import_string(logging_config)

        logging.config.dictConfig(DEFAULT_LOGGING)

        # ... then invoke it with the logging settings
        if logging_settings:
            logging_config_func(logging_settings)
