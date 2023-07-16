from enum import Enum, auto

import psycopg2

from .postgresql import get_postgresql_connection_info


class EngineKind(Enum):
    POSTGRESQL = auto()
    SQLLITE = auto()
    MSSQL = auto()


connections_pool = []


class Engine:
    def __init__(
        self, connection_properties: dict = {}, connection_string: str = ""
    ) -> None:
        self.infer_engine_kind(connection_properties, connection_string)

    def infer_engine_kind(self, connection_properties, connection_string):
        self.kind = self.get_database_kind(connection_properties, connection_string)
        match self.kind:
            case EngineKind.POSTGRESQL:
                self.connection_properties = connection_properties
                self.connection = psycopg2.connect(**self.connection_properties)

    def get_database_kind(self, connection_properties, connection_string):
        return EngineKind.POSTGRESQL


class DatabaseSession:
    def __init__(self, engine, autocommit) -> None:
        self.engine = engine
        self.autocommit = autocommit


def create_engine(connection_properties: dict = {}, connection_string: str = ""):
    if len(connection_string) > 0:
        return Engine(connection_string)
    if connection_properties:
        return Engine(connection_properties)
    raise ValueError("No connection info provided.")


def dbsession(engine, autocommit) -> list[DatabaseSession]:
    connections_pool.append(DatabaseSession(engine, autocommit))
    connections_pool = iter(connections_pool)
    yield next(connections_pool)
