from __future__ import annotations

from inspect import getmembers
from inspect import ismethod
from inspect import ismethodwrapper
from typing import List

from orm.orm import Column


class Table:

    __table_name__: str

    def __init_subclass__(cls, **kwargs) -> None:
        cls.kwargs = kwargs
        if getattr(cls, '__table_name__', False):
            return
        cls.__table_name__ = f'{cls.__name__.lower()}s'

    @classmethod
    def get_columns(self) -> list:
        cols = []
        attrs = dict(getmembers(self)).items()
        for name, field in attrs:
            if isinstance(field, Column):
                cols.append({'name': name, 'type': type(field.type)})
        return cols


def table_base():
    return Table
