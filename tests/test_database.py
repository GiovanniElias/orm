from orm.database.database import EngineKind, create_engine


def test_engine_creation_ok():
    connection_info = {
        "host": "localhost",
        "database": "postgres",
        "user": "giovannielias",
        "password": "admin",
    }
    engine = create_engine(connection_properties=connection_info)
    assert not engine.connection.closed
    assert engine.kind == EngineKind.POSTGRESQL
