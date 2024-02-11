#!/usr/bin/env python3
"""import libraries"""
import re
from typing import List
import logging
import csv
import sys
import mysql.connector
from os import environ

# Define PII Fields
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'ip')


def filter_datum(fields: List[str], redaction: str,
                message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for i in fields:
        message = re.sub(f'{i}=.*?{separator}',
            f'{i}={redaction}{separator}', message)
    return (message)


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
        """ Filters values in incoming log records using filter_datum """
        record.msg = filter_datum(self.fields, self.REDACTION,
                    record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    "takes no arguments and returns a logging.Logger object."
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handle = logging.StreamHandler()
    stream_handle.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handle)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    user_name = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    passwd = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    connect = mysql.connector.connection.MySQLConnection(
        # user="elwazeer",
        # password="elwazeer",
        # host="localhost",
        # database="holberton"
        user=user_name,
        password=passwd,
        host=host,
        database=db_name
    )

    return connect
