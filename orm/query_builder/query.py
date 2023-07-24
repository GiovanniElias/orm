from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import Any

from ..orm import Column
from .statements import *


def get_create_stmt(table_name: str, column_definitions: list[Column]):
    column_definitions_string = ', '.join(
        [str(column) for column in column_definitions],
    )
    return CREATE_TABLE_BASE_STMT.format(
        table_name=table_name, column_definitions=column_definitions_string,
    )


def get_insert_stmt(table_name: str, columns: list[Column], values: list[Any]):
    columns_string = ', '.join([col.name for col in columns])
    values_string = ', '.join(
        [f"'{val}'" for val in values if isinstance(val, str)],
    )
    return INSERT_BASE_STMT.format(
        table_name=table_name, columns=columns_string, values=values_string,
    )


def get_select_stmt(
    table_name: str,
    columns: list[Column],
    conditions: list[str] = None,
    order_by: list[Column] = None,
    ascending_order: bool = False,
    group_by: list[Column] = None,
):
    columns_string = ', '.join([col.name for col in columns])
    base = [
        SELECT_BASE_STMT.format(
            table_name=table_name, columns=columns_string,
        ),
    ]
    if conditions is not None:
        base.append(
            WHERE_CLAUSE.format(
                conditions=f' {AND} '.join(
                    [condition for condition in conditions],
                ),
            ),
        )
    if group_by is not None:
        base.append(
            GROUP_BY_CLAUSE.format(
                columns=', '.join([col.name for col in group_by]),
            ),
        )
    if order_by is not None:
        base.append(
            ORDER_BY_CLAUSE.format(
                columns=', '.join([col.name for col in order_by]),
            ),
        )
        if not ascending_order:
            base.append(DESCENDING_ORDER)
    return ' '.join(base)


def get_update_stmt():
    pass


def get_delete_stmt(table_name: str, conditions: list[Column] = None):
    base = [DELETE_BASE_STMT.format(table_name=table_name)]
    if conditions is not None:
        base.append(
            WHERE_CLAUSE.format(
                conditions=f' {AND} '.join(
                    [condition for condition in conditions],
                ),
            ),
        )
    return ' '.join(base)


def get_update_stmt(table_name: str, set_columns: list[str], conditions: list[Column] = None):
    set_columns = ', '.join([sc for sc in set_columns])
    base = [
        UPDATE_BASE_STMT.format(
            table_name=table_name, set_columns=set_columns,
        ),
    ]
    if conditions is not None:
        base.append(
            WHERE_CLAUSE.format(
                conditions=f' {AND} '.join(
                    [condition for condition in conditions],
                ),
            ),
        )
    return ' '.join(base)
