import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    db_path: Optional[str] = None
    connection_string: Optional[str] = None
    use_dbhub: bool = False


def load_database_config() -> DatabaseConfig:
    db_path = os.getenv("STUDENT_DB_PATH")
    connection_string = os.getenv("STUDENT_DB_CONNECTION_STRING")
    use_dbhub = os.getenv("STUDENT_DB_USE_DBHUB", "false").lower() in {"1", "true", "yes", "on"}

    return DatabaseConfig(
        db_path=db_path,
        connection_string=connection_string,
        use_dbhub=use_dbhub,
    )
