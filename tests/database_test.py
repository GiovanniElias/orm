from __future__ import annotations

import pytest

from orm.database.database import create_engine
from orm.database.database import dbsession
from orm.database.database import EngineKind


def test_engine_creation_postgres():
    connection_info = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'giovannielias',
        'password': 'admin',
    }
    engine = create_engine(connection_info)
    assert not engine.connection.closed
    assert engine.kind == EngineKind.POSTGRESQL


def test_create_engine_sqllite_or_mssql():
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};SERVER=test'
    with pytest.raises(NotImplementedError):
        create_engine(connection_string)


def test_create_engine_with_invalid_info():
    connection_info = 42
    with pytest.raises(ValueError):
        create_engine(connection_info)


def test_get_dbsession():
    connection_info = {
        'host': 'localhost',
        'database': 'postgres',
        'user': 'giovannielias',
        'password': 'admin',
    }
    engine = create_engine(connection_info)
    session = dbsession(engine=engine, autocommit=False)
    assert not session.database.engine.connection.closed
