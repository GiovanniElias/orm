import psycopg2
from database.lib import is_postgresql_db
from enum import Enum, auto
from postgresql import PostgresqlConnectionInfo


class DatabaseKind:
    POSTGRESQL = auto()
    SQLLITE = auto()
    MSSQL = auto()


class DatabaseSession:
    def __init__(self, *args, **kwargs) -> None:
        self.infer_engine_kind(**kwargs)
    

    def infer_engine_kind(self, *args, **kwargs):
        kind = self.get_database_kind()
        match kind:
            case DatabaseKind.POSTGRESQL:
                
                postgresql_connection_info = PostgresqlConnectionInfo(**kwargs)
                self.connection = psycopg2.connect()
    

    def get_database_kind(self):
        return DatabaseKind.POSTGRESQL



def sessionmaker(engine) -> DatabaseSession:
    return DatabaseSession(engine)






    