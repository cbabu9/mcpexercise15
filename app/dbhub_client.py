import os
from typing import Optional


class DBHubClient:
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or os.getenv("STUDENT_DB_CONNECTION_STRING")

    def is_configured(self) -> bool:
        return bool(self.connection_string)

    def get_connection_info(self) -> dict:
        return {
            "connection_string": self.connection_string,
            "configured": self.is_configured(),
        }
