from __future__ import annotations

from orm.orm import Column
from orm.table.table import table_base
from orm.types import Integer


def test_table_base_object_creation():
    Base = table_base()

    class User(Base):
        id = Column(type=Integer(), name='id')

    table_name = 'users'
    columns = [{'name': 'id', 'type': Integer}]

    assert User.__dict__['__table_name__'] == table_name
    assert User.get_columns() == columns
