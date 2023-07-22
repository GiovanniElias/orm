from __future__ import annotations

import pytest
from pydantic import ValidationError

from orm.orm import Column
from orm.table.table import table_base
from orm.types import Integer

Base = table_base()


def test_table_base_object_creation():

    class User(Base):
        id = Column(type=Integer(), name='id')

    expected_table_name = 'users'
    expected_columns = [{'name': 'id', 'type': Integer}]

    table_name = User.__dict__['__table_name__']
    columns = User.get_columns()

    assert table_name == expected_table_name
    assert columns == expected_columns


def test_table_creation_with_untyped_column():
    with pytest.raises(ValidationError):
        class User(Base):
            id = Column(name='id')


def test_table_creation_without_column_name():
    class User(Base):
        id = Column(type=Integer())

    expected_id_col_name = 'id'
    id_col_name = User.id.name

    assert id_col_name == expected_id_col_name


def test_no_two_columns_have_the_same_name():

    with pytest.raises(NameError):
        class User(Base):
            id = Column(type=Integer())
            id2 = Column(type=Integer(), name='id')
