import unittest

from app.api import ApiError, StudentApi


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = StudentApi()

    def test_create_and_list_students(self) -> None:
        response = self.api.create_student({"name": "Mina"})
        self.assertEqual(response["name"], "Mina")

        listed = self.api.list_students()
        self.assertIn("students", listed)

    def test_create_course_with_validation(self) -> None:
        with self.assertRaises(ApiError):
            self.api.create_course({"title": "   "})


if __name__ == "__main__":
    unittest.main()
