from __future__ import annotations

from dataclasses import field
from datetime import date
from datetime import datetime
from typing import Any
from typing import Optional

from pydantic import BaseModel
from pydantic import field_validator


class ColumnType(BaseModel):
    _python_type: Any
    _alias: str


class Column(BaseModel):
    name: str = field(default=None)
    type: ColumnType
    primary_key: bool = field(default=False)
    nullable: bool = field(default=True)
    default: Any = field(default=None)

    def __repr__(self) -> str:
        base = f'{self.name} {self.type._alias}'
        if self.primary_key:
            base += f' PRIMARY KEY'
        if not self.nullable and not self.primary_key:
            base += ' NOT NULL'
        if self.default is not None:
            base += f' DEFAULT {self.default}'
        return base.rstrip()

    def comparison(self, value: object, operator: str):
        if isinstance(value, (str, date, datetime)):
            return f"{self.name} {operator} '{value}'"
        return f'{self.name} {operator} {value}'

    def __eq__(self, value: object) -> str:
        return self.comparison(value, '=')

    def __ne__(self, value: object) -> str:
        return self.comparison(value, '<>')

    def __gt__(self, value: object) -> str:
        return self.comparison(value, '>')

    def __lt__(self, value: object) -> str:
        return self.comparison(value, '<')

    def __ge__(self, value: object) -> str:
        return self.comparison(value, '>=')

    def __le__(self, value: object) -> str:
        return self.comparison(value, '<=')
