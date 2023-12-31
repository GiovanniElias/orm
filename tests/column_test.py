from __future__ import annotations

from orm.orm import Column
from orm.types import Integer


def test_column_string_stresentation():
    col_pk = Column(
        name='test',
        type=Integer(),
        nullable=False,
        primary_key=True,
    )
    col_not_null = Column(
        name='test',
        type=Integer(),
        nullable=False,
        primary_key=False,
    )
    col_with_default = Column(
        name='test',
        type=Integer(),
        nullable=False,
        primary_key=False,
        default='default',
    )
    expected_col_str_str_pk = 'test INT PRIMARY KEY'
    expected_col_str_str_nn = 'test INT NOT NULL'
    expected_col_str_str_de = 'test INT NOT NULL DEFAULT default'

    assert str(col_pk) == expected_col_str_str_pk
    assert str(col_not_null) == expected_col_str_str_nn
    assert str(col_with_default) == expected_col_str_str_de


def test_comparison():
    col = Column(name='test', type=Integer(), nullable=False, primary_key=True)
    value = 45
    condition_ne = col != value
    condition_e = col == value
    condition_ge = col >= value
    condition_le = col <= value
    condition_gt = col > value
    condition_lt = col < value

    expected_condition_ne = 'test <> 45'
    expected_condition_e = 'test = 45'
    expected_condition_ge = 'test >= 45'
    expected_condition_le = 'test <= 45'
    expected_condition_gt = 'test > 45'
    expected_condition_lt = 'test < 45'

    assert condition_ne == expected_condition_ne
    assert condition_e == expected_condition_e
    assert condition_ge == expected_condition_ge
    assert condition_le == expected_condition_le
    assert condition_gt == expected_condition_gt
    assert condition_lt == expected_condition_lt


def test_translation_to_db_dialects():
    pass
