from __future__ import annotations

from .orm import ColumnType


class Integer(ColumnType):
    _python_type = int
    _alias = 'INT'
