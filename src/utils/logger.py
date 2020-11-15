from logging import config
import logging, sys


class Logger:
    def __init__(self):
        self.logger = None

        self.logger_name = None
        self.logger_level = None
        self.logger_address = None
        self.logger_facility = None

    def config_logger(self, conf):
        section_name = 'LOGGER'
        self.logger_name = conf.get(section_name, 'LOG_NAME')
        self.logger_level = conf.get(section_name, 'LOG_LEVEL')
        self.logger_address = conf.get(section_name, 'LOG_ADDRESS')
        self.logger_facility = conf.get(section_name, 'LOG_FACILITY')

        switcher = {
            'CRITICAL': logging.CRITICAL,
            'FATAL': logging.FATAL,
            'ERROR': logging.ERROR,
            'WARNING': logging.WARNING,
            'WARN': logging.WARN,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG,
            'NOTSET': logging.NOTSET,
        }
        LEVEL = switcher.get(self.logger_level, logging.NOTSET)

        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '%(name)s %(levelname)s P%(process)d T%(thread)d %(message)s'
                },
            },
            'handlers': {
                'stdout': {
                    'class': 'logging.StreamHandler',
                    'stream': sys.stdout,
                    'formatter': 'verbose',
                },
                'sys-logger': {
                    'class': 'logging.handlers.SysLogHandler',
                    'address': self.logger_address,
                    'facility': self.logger_facility,
                    'formatter': 'verbose',
                },
            },
            'loggers': {
                self.logger_name: {
                    'handlers': ['sys-logger', 'stdout'],
                    'level': LEVEL,
                    'propagate': True,
                },
            }
        }

        config.dictConfig(LOGGING)

        self.logger = logging.getLogger(self.logger_name)

        self.info('LOGGER --> '+
                  '\n\tlogger_name: ' + self.logger_name +
                  '\n\tlogger_level: ' + self.logger_level +
                  '\n\tlogger_facility: ' + self.logger_facility +
                  '\n\tlogger_address: ' + self.logger_address)

    def critical(self, msg):
        self.logger.critical(msg)

    def error(self, msg):
        self.logger.error(msg)

    def exception(self, msg, exc_info=True):
        self.logger.exception(msg, exc_info=exc_info)

    def warning(self, msg):
        self.logger.warning(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

logger = Logger()