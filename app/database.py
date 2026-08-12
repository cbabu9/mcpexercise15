import os
import sqlite3
import threading
from typing import Dict, Optional

from app.config import load_database_config
from app.dbhub_client import DBHubClient


class DatabaseManager:
    _connections: threading.local = threading.local()
    _dbhub_client: Optional[DBHubClient] = None

    @classmethod
    def _resolve_db_path(cls, db_path: Optional[str] = None) -> str:
        config = load_database_config()
        if db_path is None:
            db_path = config.db_path or os.path.join(os.getcwd(), "student_database.db")
        return db_path

    @classmethod
    def get_connection(cls, db_path: Optional[str] = None) -> sqlite3.Connection:
        resolved_path = cls._resolve_db_path(db_path)
        connections: Dict[str, sqlite3.Connection] = getattr(cls._connections, "connections", {})
        if resolved_path not in connections:
            config = load_database_config()
            if config.use_dbhub and config.connection_string:
                cls._dbhub_client = DBHubClient(config.connection_string)
                conn = sqlite3.connect(resolved_path, check_same_thread=False)
            else:
                conn = sqlite3.connect(resolved_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            cls._initialize_schema(conn)
            connections[resolved_path] = conn
            cls._connections.connections = connections
        return connections[resolved_path]

    @classmethod
    def initialize(cls, db_path: Optional[str] = None) -> sqlite3.Connection:
        return cls.get_connection(db_path)

    @classmethod
    def _has_schema(cls, conn: sqlite3.Connection) -> bool:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='students'"
        )
        return cursor.fetchone() is not None

    @classmethod
    def _initialize_schema(cls, conn: sqlite3.Connection) -> None:
        if cls._has_schema(conn):
            return

        schema_path = os.path.join(os.path.dirname(__file__), "..", "sql", "init_schema.sql")
        sample_data_path = os.path.join(os.path.dirname(__file__), "..", "sql", "sample_data.sql")

        with open(schema_path, "r", encoding="utf-8") as schema_file:
            conn.executescript(schema_file.read())

        with open(sample_data_path, "r", encoding="utf-8") as sample_file:
            conn.executescript(sample_file.read())

        conn.commit()
