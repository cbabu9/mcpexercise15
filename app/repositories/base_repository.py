import sqlite3
from typing import Optional

from app.database import DatabaseManager


class BaseRepository:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        return DatabaseManager.get_connection(self.db_path)
