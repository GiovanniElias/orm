from __future__ import annotations

from datetime import date
from datetime import datetime

from .orm import ColumnType


class Integer(ColumnType):
    _python_type = int
    _alias = 'INT'


class String(ColumnType):
    _python_type = str
    _alias = 'VARCHAR(255)'


class Date(ColumnType):
    _python_type = date
    _alias = 'DATE'


class DateTime(ColumnType):
    _python_type = datetime
    _alias = 'TIMESTAMP'


class Bool(ColumnType):
    _python_type = bool
    _alias = 'BOOLEAN'
