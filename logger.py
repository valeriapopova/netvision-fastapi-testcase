import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler


class CustomLogger:
    def __init__(self):
        self.format = logging.Formatter(
            '%(asctime)s: [%(levelname)s] %(message)s'
        )
        self.evt = self.create_logger('event', logging.INFO)
        self.err = self.create_logger('error', logging.ERROR, False)
        self.err_count = 0

    def file_handler(self, name: str, level: int):
        fname = f'_logs/{name}.log'
        handler = TimedRotatingFileHandler(
            filename=fname,
            when='midnight',
            interval=1,
            backupCount=15,
            encoding='utf-8',
            delay=True,
        )
        handler.setLevel(level)
        handler.setFormatter(self.format)
        return handler

    def stdout_handler(self):
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.format)
        return handler

    def create_logger(self, name: str, level: str, stdout: bool = True):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(self.file_handler(name, level))
        if stdout is True:
            logger.addHandler(self.stdout_handler())
        return logger

    def rec_error(self, msg: str):
        self.err_count += 1
        self.evt.error(msg)
        self.err.error(msg, exc_info=True)
