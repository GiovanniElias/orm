from typing import Optional
from pydantic import BaseModel, ValidationError

class PostgresqlConnectionInfo(BaseModel):
    host: str
    database: str
    user: str
    password: str
    port: Optional[str]

def get_postgresql_connection_info(*args, **kwargs):
    try:
        if 
        info = PostgresqlConnectionInfo(**kwargs)
    except ValidationError:
        pass


















