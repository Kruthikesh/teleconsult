import os
from datetime import datetime

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# the minimum reported level
if DEBUG:
    min_level = 'DEBUG'
else:
    min_level = 'INFO'

# the minimum reported level for Django's modules
# optionally set to DEBUG to see database queries etc.
# or set to min_level to control it using the DEBUG flag
min_django_level = 'INFO'
log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
info_path = os.path.join(log_path, 'info')
error_path = os.path.join(log_path, 'error')
warning_path = os.path.join(log_path, 'warning')
critical_path = os.path.join(log_path, 'critical')
debug_path = os.path.join(log_path, 'debug')

current_time = datetime.now()
current_date = current_time.strftime("%Y-%m-%d")  # %H:%M
logger_file_name = str(current_date) + '.log'

# logging dictConfig configuration
logging = {
    'version': 1,
    'disable_existing_loggers': False,  # keep Django's default loggers
    'formatters': {
        # see full list of attributes here:
        # https://docs.python.org/3/library/logging.html#logrecord-attributes
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'timestampthread': {
            'format': "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [%(name)-20.20s]  %(message)s",
        },
    },
    'handlers': {
        'logfile_info': {
            # optionally raise to INFO to not fill the log file too quickly
            'level': 'INFO',  # this level or higher goes to the log file
            'class': 'logging.handlers.RotatingFileHandler',
            # IMPORTANT: replace with your desired logfile name!
            'filename': os.path.join(info_path, logger_file_name),
            'maxBytes': 50 * 10 ** 6,  # will 50 MB do?
            'backupCount': 3,  # keep this many extra historical files
            'formatter': 'timestampthread'
        },
        'logfile_error': {
            # optionally raise to INFO to not fill the log file too quickly
            'level': 'ERROR',  # this level or higher goes to the log file
            'class': 'logging.handlers.RotatingFileHandler',
            # IMPORTANT: replace with your desired logfile name!
            'filename': os.path.join(error_path, logger_file_name),
            'maxBytes': 50 * 10 ** 6,  # will 50 MB do?
            'backupCount': 3,  # keep this many extra historical files
            'formatter': 'timestampthread'
        },
        'logfile_warning': {
            # optionally raise to INFO to not fill the log file too quickly
            'level': 'WARNING',  # this level or higher goes to the log file
            'class': 'logging.handlers.RotatingFileHandler',
            # IMPORTANT: replace with your desired logfile name!
            'filename': os.path.join(warning_path, logger_file_name),
            'maxBytes': 50 * 10 ** 6,  # will 50 MB do?
            'backupCount': 3,  # keep this many extra historical files
            'formatter': 'timestampthread'
        },
        'logfile_critical': {
            # optionally raise to INFO to not fill the log file too quickly
            'level': 'CRITICAL',  # this level or higher goes to the log file
            'class': 'logging.handlers.RotatingFileHandler',
            # IMPORTANT: replace with your desired logfile name!
            'filename': os.path.join(critical_path, logger_file_name),
            'maxBytes': 50 * 10 ** 6,  # will 50 MB do?
            'backupCount': 3,  # keep this many extra historical files
            'formatter': 'timestampthread'
        },
        'logfile_debug': {
            # optionally raise to INFO to not fill the log file too quickly
            'level': 'DEBUG',  # this level or higher goes to the log file
            'class': 'logging.handlers.RotatingFileHandler',
            # IMPORTANT: replace with your desired logfile name!
            'filename': os.path.join(debug_path, logger_file_name),
            'maxBytes': 50 * 10 ** 6,  # will 50 MB do?
            'backupCount': 3,  # keep this many extra historical files
            'formatter': 'timestampthread'
        },
        'console': {
            'level': min_level,  # this level or higher goes to the console
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {  # configure all of Django's loggers
            'handlers': ['logfile_info', 'logfile_error', 'logfile_warning', 'logfile_critical', 'logfile_debug',
                         'console'],
            'level': min_django_level,  # this level or higher goes to console and logfile
            'propagate': False,  # don't propagate further, to avoid duplication
        },
        'django.db.backends': {
            'handlers': ['logfile_info', 'logfile_error', 'logfile_warning', 'logfile_critical', 'logfile_debug',
                         'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        # root configuration – for all of our own apps
        # (feel free to do separate treatment for e.g. brokenapp vs. sth else)
        '': {
            'handlers': ['logfile_info', 'logfile_error', 'logfile_warning', 'logfile_critical', 'logfile_debug',
                         'console'],
            'level': min_level,  # this level or higher goes to the console and logfile
        },
    },
}
