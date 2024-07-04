#!/usr/bin/env python3
""" module to define a function called filter_datum
that returns the log message obfuscated:
"""
from typing import List
import re
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ function that returns the log message obfuscated """
    for field in fields:
        message = re.sub(
            rf'{field}=.*?{separator}',
            f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ method that filters values in incoming log records """
        return filter_datum(
            self.fields, self.REDACTION,
            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ returns a Logger object with the required configs """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(log_handler)
    return logger
