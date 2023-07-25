from __future__ import annotations

from enum import auto
from enum import Enum
from typing import Any

import psycopg2
from typing_extensions import override

from .postgresql import get_postgresql_connection_info
from orm.orm import Column
from orm.query_builder.query import get_create_stmt
from orm.query_builder.query import get_delete_stmt
from orm.query_builder.query import get_insert_stmt
from orm.query_builder.query import get_select_stmt
from orm.query_builder.query import get_update_stmt
from orm.table.table import Table


class EngineKind(Enum):
    POSTGRESQL = auto()
    SQLLITE = auto()
    MSSQL = auto()


connections_pool = []


def database_transaction(func):
    def execute_statement(*args, **kwargs):
        self = args[0]
        connection = self.connect()
        statement = func(*args)
        try:
            with connection.cursor() as cursor:
                cursor.execute(statement)
                return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            connection.commit()
            connection.close()
    return execute_statement


class Engine:
    def __init__(self, connection_info: dict | str) -> None:
        self.connection_info = connection_info
        self.infer_engine_kind(connection_info)

    def connect_psotgresql(self):
        return psycopg2.connect(**self.connection_info)

    def infer_engine_kind(self, connection_info):
        self.kind = self._get_database_kind(connection_info)
        match self.kind:
            case EngineKind.POSTGRESQL:
                self.connect = self.connect_psotgresql
            case EngineKind.MSSQL:
                raise NotImplementedError()
            case EngineKind.SQLLITE:
                raise NotImplementedError()

    def _get_database_kind(self, connection_info: dict | str):
        if isinstance(connection_info, dict):
            return EngineKind.POSTGRESQL
        if connection_info.startswith('Driver'):
            return EngineKind.MSSQL
        return EngineKind.SQLLITE

    @database_transaction
    def create(self, table: Table):
        table_name = table.__table_name__
        column_definitions = table.get_columns()
        return get_create_stmt(table_name, column_definitions)

    @database_transaction
    def insert(self, table: Table, values: list[Any], columns: list[Column] = None):
        table_name = table.__table_name__
        columns = columns if columns is not None else table.get_columns()
        return get_insert_stmt(table_name, columns, values)

    @database_transaction
    def select(
        self,
        table: Table,
        columns: list[Column] = None,
        conditions: list[str] = None,
        order_by: list[Column] = None,
        ascending_order: bool = False,
        group_by: list[Column] = None,
    ):
        table_name = table.__table_name__
        columns = columns if columns is not None else table.get_columns()
        return get_select_stmt(
            table_name, columns, conditions, order_by, ascending_order, group_by
        )

    @database_transaction
    def update(
        self,
        table: Table,
        set_columns: list[str],
        conditions: list[str],
    ):
        table_name = table.__table_name__
        return get_update_stmt(table_name, set_columns, conditions)

    @database_transaction
    def delete(
        self,
        table: Table,
        conditions: list[str],
    ):
        table_name = table.__table_name__
        return get_delete_stmt(table_name, conditions)


class DatabaseSession:
    def __init__(self, database) -> None:
        self.database = database


class Database:
    def __init__(self, engine: Engine, autocommit) -> None:
        self.engine = engine
        self.autocommit = autocommit
        self.tables = []
        # TODO: GET DB NAME. MIGHT HAVE TO CREATE DIFFERENT KINDS OF ENGINES.
        self.name = ''

    # TODO: group all stmt methods into another class and inject into db class through a factory
    def create(self, table: Table):
        return self.engine.create(table)

    def insert(self, table: Table, values: list[Any], columns: list[Column] = None):
        return self.engine.insert(table, values, columns)

    def select(
        self,
        table: Table,
        columns: list[Column] = None,
        conditions: list[str] = None,
        order_by: list[Column] = None,
        ascending_order: bool = False,
        group_by: list[Column] = None,
    ):
        return self.engine.select(
            table, columns, conditions, order_by, ascending_order, group_by
        )

    def update(self):
        return self.engine.update()

    def delete(self, table: Table, conditions: list[str]):
        return self.engine.delete(table, conditions)


def create_engine(connection_info: dict | str):
    valid_format = isinstance(connection_info, (dict, str))
    if not connection_info or not valid_format:
        raise ValueError(
            'No connection info provided or info has wrong format.')
    return Engine(connection_info)


def dbsession(engine, autocommit) -> DatabaseSession:
    # TODO: ADD POOL LOGIC, EVEN IF BASIC
    engine_is_valid = True
    if not engine_is_valid:
        raise ConnectionError('Engine is not valid.')
    database = Database(engine, autocommit)
    return DatabaseSession(database)
