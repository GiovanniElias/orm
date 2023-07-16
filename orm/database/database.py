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
        self, connection_info: dict | str
    ) -> None:
        self.infer_engine_kind(connection_info)

    def infer_engine_kind(self, connection_info):
        self.kind = self._get_database_kind(connection_info)
        match self.kind:
            case EngineKind.POSTGRESQL:
                self.connection_info = connection_info
                self.connection = psycopg2.connect(**self.connection_info)
            case EngineKind.MSSQL:
                raise NotImplementedError()
            case EngineKind.SQLLITE:
                raise NotImplementedError()

    def _get_database_kind(self, connection_info: dict | str):
        if isinstance(connection_info, dict):
            return EngineKind.POSTGRESQL
        if connection_info.startswith("Driver"):
            return EngineKind.MSSQL
        return EngineKind.SQLLITE


class DatabaseSession:
    def __init__(self, engine, autocommit) -> None:
        self.engine = engine
        self.autocommit = autocommit


def create_engine(connection_info: dict | str):
    valid_format = type(connection_info) in (dict, str)
    if not connection_info or not valid_format:
        raise ValueError("No connection info provided.")
    return Engine(connection_info)
    


def dbsession(engine, autocommit) -> DatabaseSession:
    #TODO: ADD POOL LOGIC, EVEN IF BASIC
    engine_is_valid = True
    if not engine_is_valid:
        raise ConnectionError("Engine is not valid.")
    return DatabaseSession(engine, autocommit)
