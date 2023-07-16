from orm.database.database import EngineKind, create_engine, dbsession
import pytest

def test_engine_creation_postgres():
    connection_info = {
        "host": "localhost",
        "database": "postgres",
        "user": "giovannielias",
        "password": "admin",
    }
    engine = create_engine(connection_info)
    assert not engine.connection.closed
    assert engine.kind == EngineKind.POSTGRESQL


def test_create_engin_sqllite_or_mssql():
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};SERVER=test'
    with pytest.raises(NotImplementedError):
        create_engine(connection_string)


def test_get_dbsession():
    connection_info = {
        "host": "localhost",
        "database": "postgres",
        "user": "giovannielias",
        "password": "admin",
    }
    engine = create_engine(connection_info)
    session = dbsession(engine=engine, autocommit=False)
    assert not session.engine.connection.closed