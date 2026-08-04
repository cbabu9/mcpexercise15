import os
import tempfile
import unittest

from app.database import DatabaseManager
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.student_repository import StudentRepository
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.services.student_service import StudentService


class StudentDatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp_dir.name, "test_student.db")
        DatabaseManager.initialize(self.db_path)

        self.student_service = StudentService(StudentRepository(self.db_path))
        self.course_service = CourseService(CourseRepository(self.db_path))
        self.enrollment_service = EnrollmentService(
            EnrollmentRepository(self.db_path),
            StudentRepository(self.db_path),
            CourseRepository(self.db_path),
        )

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def test_create_and_list_student(self) -> None:
        initial_count = len(self.student_service.list_students())
        student = self.student_service.create_student("Ada Lovelace")

        self.assertEqual(student.name, "Ada Lovelace")
        self.assertEqual(len(self.student_service.list_students()), initial_count + 1)

    def test_create_course_and_enroll_student(self) -> None:
        initial_enrollment_count = len(self.enrollment_service.list_enrollments())
        student = self.student_service.create_student("Grace Hopper")
        course = self.course_service.create_course("Algorithms")
        enrollment = self.enrollment_service.enroll_student(student.id, course.id)

        self.assertEqual(enrollment.student_id, student.id)
        self.assertEqual(enrollment.course_id, course.id)
        self.assertEqual(len(self.enrollment_service.list_enrollments()), initial_enrollment_count + 1)

    def test_initialization_creates_schema_and_sample_data(self) -> None:
        self.assertGreaterEqual(len(self.student_service.list_students()), 2)
        self.assertGreaterEqual(len(self.course_service.list_courses()), 2)
        self.assertGreaterEqual(len(self.enrollment_service.list_enrollments()), 2)

    def test_repeated_initialization_is_idempotent(self) -> None:
        DatabaseManager.initialize(self.db_path)
        DatabaseManager.initialize(self.db_path)

        self.assertEqual(len(self.student_service.list_students()), 2)
        self.assertEqual(len(self.course_service.list_courses()), 2)
        self.assertEqual(len(self.enrollment_service.list_enrollments()), 2)


if __name__ == "__main__":
    unittest.main()
