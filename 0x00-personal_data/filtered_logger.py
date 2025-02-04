#!/usr/bin/env python3
""" module to define a function called filter_datum
that returns the log message obfuscated:
"""
from typing import List
import re
import logging
from mysql.connector import MySQLConnection, connect
from os import getenv


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


def get_db() -> MySQLConnection:
    """ returns a connection to a secure 'holberton' database
    to read a users table """
    if getenv('PERSONAL_DATA_DB_NAME') is None:
        raise ValueError("database name is not set in environment")
    return connect(
        user=getenv('PERSONAL_DATA_DB_USERNAME', "root"),
        password=getenv('PERSONAL_DATA_DB_PASSWORD', ""),
        host=getenv('PERSONAL_DATA_DB_HOST', "localhost"),
        database=getenv('PERSONAL_DATA_DB_NAME'),
        port=3306,
        )


def main():
    """ the main function that retrieves all rows from the users table
    and print them with the PII obfuscated"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        message = "{}; {}; {}; {}; {}; {}; {}; {};".format(
            f"name={row[0]}",
            f"email={row[1]}",
            f"phone={row[2]}",
            f"ssn={row[3]}",
            f"password={row[4]}",
            f"ip={row[5]}",
            f"last_login={row[6]}",
            f"user_agent={row[7]}"
            )
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
