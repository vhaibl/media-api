import logging
import os
import sys


class OnlyErrorCriticalFilter(logging.Filter):
    def filter(self, record):
        """
        ERROR or CRITICAL
        :param record:
        :return: False - выбрасывать, True - оставлять
        """
        return record.levelno == logging.ERROR or record.levelno == logging.CRITICAL


class OnlyDebugWarningFilter(logging.Filter):
    def filter(self, record):
        """
        DEBUG or WARNING
        :param record:
        :return: False - выбрасывать, True - оставлять
        """
        return record.levelno == logging.DEBUG or record.levelno == logging.WARNING


class OnlyInfoFilter(logging.Filter):
    def filter(self, record):
        """
        INFO
        :param record:
        :return: False - выбрасывать, True - оставлять
        """
        return record.levelno == logging.INFO


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'only_error_critical': {
            '()': 'media_logging.OnlyErrorCriticalFilter',
        },
        'only_debug_warning': {
            '()': 'media_logging.OnlyDebugWarningFilter',
        },
        'only_info': {
            '()': 'media_logging.OnlyInfoFilter',
        }
    },
    'handlers': {
        'file_debug': {
            'class': "logging.FileHandler",
            'formatter': "default",
            'filename': os.path.join(sys.path[0], 'log', 'debug.log'),
            'encoding': 'utf-8',
            'mode': 'w',
            'filters': ['only_debug_warning']
        },
        'file_error': {
            'class': "logging.FileHandler",
            'formatter': "default",
            'filename': os.path.join(sys.path[0], 'log', 'error.log'),
            'encoding': 'utf-8',
            'mode': 'w',
            'filters': ['only_error_critical']
        },
        'file_info': {
            'class': "logging.FileHandler",
            'formatter': "default",
            'filename': os.path.join(sys.path[0], 'log', 'info.log'),
            'encoding': 'utf-8',
            'mode': 'w',
            'filters': ['only_info']
        }
    },
    'loggers': {
        'api': {
            'handlers': ['file_debug', 'file_error', 'file_info'],
            'level': 'DEBUG',  # 'DEBUG', 'ERROR'
        }
    },
    'formatters': {
        'default': {'format': "%(asctime)s|%(name)s|%(levelname)s|%(message)s"},
    },
}
