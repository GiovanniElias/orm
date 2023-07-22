from __future__ import annotations

from dataclasses import field
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
