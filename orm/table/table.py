from __future__ import annotations

from inspect import getmembers
from inspect import ismethod
from inspect import ismethodwrapper
from typing import List

from orm.orm import Column


class Table:

    __table_name__: str

    def __init_subclass__(cls, **kwargs) -> None:
        cls.attrs = dict(getmembers(cls)).items()
        cls.kwargs = kwargs
        cls._assign_table_name()
        cls._assign_column_names()
        cls._validate_column_names()

    @classmethod
    def _assign_table_name(cls):
        if getattr(cls, '__table_name__', False):
            return
        cls.__table_name__ = f'{cls.__name__.lower()}s'

    @classmethod
    def _assign_column_names(cls):
        for name, field in cls.attrs:
            if isinstance(field, Column) and field.name is None:
                field.name = name

    @classmethod
    def get_columns(cls) -> list:
        cols = []
        for name, field in cls.attrs:
            if isinstance(field, Column):
                cols.append({'name': field.name, 'type': type(field.type)})
        return cols

    @classmethod
    def _validate_column_names(cls):
        # TODO: REPLACE NAIVE IMPLEMENTATION
        cols = cls.get_columns()
        names = []
        for col in cols:
            name = col.get('name')
            if name not in names:
                names.append(name)
            else:
                raise NameError('No two columns should share names.')


def table_base():
    return Table
