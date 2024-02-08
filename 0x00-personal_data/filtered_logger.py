#!/usr/bin/env python3
"""import libraries"""
import re


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    for i in fields:
        message = re.sub(f'{i}=.*?{separator}',
            f'{i}={redaction}{separator}', message)
    return (message)
