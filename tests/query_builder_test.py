from __future__ import annotations

from orm.orm import Column
from orm.query_builder.query import get_create_stmt
from orm.query_builder.query import get_delete_stmt
from orm.query_builder.query import get_insert_stmt
from orm.query_builder.query import get_select_stmt
from orm.query_builder.query import get_update_stmt
from orm.types import Integer
from orm.types import String


def test_create_stmt_creation():
    test_table_name = 'test'
    column_definitions = [
        Column(type=Integer(), name='id'),
        Column(
            type=String(), name='test',
            default='test_default', primary_key=True,
        ),
    ]
    expected_stmt = 'CREATE TABLE [IF NOT EXISTS] test (id INT, test VARCHAR(MAX) PRIMARY KEY DEFAULT test_default);'
    stmt = get_create_stmt(
        table_name=test_table_name, column_definitions=column_definitions,
    )
    assert stmt == expected_stmt


def test_insert_stmt_creation():
    test_table_name = 'test'
    columns = [
        Column(type=Integer(), name='id'),
        Column(
            type=String(), name='test',
            default='test_default', primary_key=True,
        ),
    ]
    values = ['a1b2c3d4', 'testeroni']
    expected_stmt = "INSERT INTO test (id, test) VALUES ('a1b2c3d4', 'testeroni');"
    stmt = get_insert_stmt(
        table_name=test_table_name,
        columns=columns, values=values,
    )
    assert stmt == expected_stmt


def test_select_no_filter_stmt_creation():
    test_table_name = 'test'
    columns = [
        Column(type=Integer(), name='id'),
        Column(
            type=String(), name='test',
            default='test_default', primary_key=True,
        ),
    ]
    expected_stmt = 'SELECT id, test FROM test'
    stmt = get_select_stmt(table_name=test_table_name, columns=columns)
    assert stmt == expected_stmt


def test_select_complete_stmt_creation():
    test_table_name = 'test'
    columns = [
        Column(type=Integer(), name='id'),
        Column(
            type=String(), name='test',
            default='test_default', primary_key=True,
        ),
        Column(name='name', type=Integer(), nullable=False, primary_key=False),
    ]
    conditions = [
        Column(type=Integer(), name='id') == 'a1b2c3d4',
        Column(
            type=String(), name='test',
            default='test_default', primary_key=True,
        )
        != None,
    ]
    order_by = [
        Column(
            name='name', type=Integer(),
            nullable=False, primary_key=False,
        ),
    ]
    ascending_order = False
    group_by = [
        Column(
            name='name', type=Integer(),
            nullable=False, primary_key=False,
        ),
    ]

    expected_stmt = "SELECT id, test, name FROM test WHERE id = 'a1b2c3d4' AND test <> NULL GROUP BY name ORDER BY name DESC"

    assert all([isinstance(x, str) for x in conditions]) == True

    stmt = get_select_stmt(
        table_name=test_table_name,
        columns=columns,
        conditions=conditions,
        order_by=order_by,
        ascending_order=ascending_order,
        group_by=group_by,
    )
    assert stmt == expected_stmt


def test_delete_stmt_creation():
    test_table_name = 'test'
    conditions = [
        Column(type=Integer(), name='id') == 'a1b2c3d4',
        Column(
            type=String(), name='test',
            default='test_default', primary_key=True,
        )
        != None,
    ]
    expected_no_filter = 'DELETE FROM test'
    expected_with_filter = "DELETE FROM test WHERE id = 'a1b2c3d4' AND test <> NULL"

    stmt_no_filter = get_delete_stmt(table_name=test_table_name)
    stmt_with_filter = get_delete_stmt(
        table_name=test_table_name, conditions=conditions,
    )

    assert stmt_no_filter == expected_no_filter
    assert stmt_with_filter == expected_with_filter


def test_update_stmt_creation():
    test_table_name = 'test'
    set_columns = [
        Column(type=Integer(), name='id') == 'x', Column(
            type=String(), name='test',
            default='test_default', primary_key=True,
        ) == 4,
    ]
    conditions = [
        Column(type=Integer(), name='id') == 'a1b2c3d4',
        Column(
            type=String(), name='test',
            default='test_default', primary_key=True,
        )
        != None,
    ]
    expected_no_filter = "UPDATE test SET id = 'x', test = 4"
    expected_with_filter = "UPDATE test SET id = 'x', test = 4 WHERE id = 'a1b2c3d4' AND test <> NULL"

    stmt_no_filter = get_update_stmt(
        table_name=test_table_name, set_columns=set_columns,
    )
    stmt_with_filter = get_update_stmt(
        table_name=test_table_name, set_columns=set_columns, conditions=conditions,
    )

    assert stmt_no_filter == expected_no_filter
    assert stmt_with_filter == expected_with_filter
