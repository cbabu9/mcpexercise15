import os
import unittest

from app.config import load_database_config


class DatabaseConfigTests(unittest.TestCase):
    def test_load_database_config_reads_environment(self) -> None:
        os.environ["STUDENT_DB_PATH"] = "/tmp/demo.db"
        os.environ["STUDENT_DB_CONNECTION_STRING"] = "dbhub://demo"
        os.environ["STUDENT_DB_USE_DBHUB"] = "true"

        config = load_database_config()

        self.assertEqual(config.db_path, "/tmp/demo.db")
        self.assertEqual(config.connection_string, "dbhub://demo")
        self.assertTrue(config.use_dbhub)


if __name__ == "__main__":
    unittest.main()
