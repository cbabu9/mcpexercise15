import sqlite3
from typing import Optional

from app.database import DatabaseManager


class BaseRepository:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.connection = DatabaseManager.get_connection(db_path)

    def _connect(self) -> sqlite3.Connection:
        if self.connection is None:
            self.connection = DatabaseManager.get_connection(self.db_path)
        return self.connection
