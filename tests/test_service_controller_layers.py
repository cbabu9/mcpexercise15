import io
import unittest
from contextlib import redirect_stdout

from app.controllers.student_controller import StudentController
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.services.student_service import StudentService


class FakeStudentRepository:
    def __init__(self) -> None:
        self._students = []
        self._next_id = 1

    def create(self, name: str) -> Student:
        student = Student(id=self._next_id, name=name)
        self._next_id += 1
        self._students.append(student)
        return student

    def get_by_id(self, student_id: int):
        for student in self._students:
            if student.id == student_id:
                return student
        return None

    def list_all(self):
        return list(self._students)

    def update(self, student_id: int, name: str) -> Student:
        student = self.get_by_id(student_id)
        if student is None:
            raise ValueError("Student not found")
        student.name = name
        return student

    def delete(self, student_id: int) -> None:
        self._students = [student for student in self._students if student.id != student_id]


class FakeCourseRepository:
    def __init__(self) -> None:
        self._courses = []
        self._next_id = 1

    def create(self, title: str) -> Course:
        course = Course(id=self._next_id, title=title)
        self._next_id += 1
        self._courses.append(course)
        return course

    def get_by_id(self, course_id: int):
        for course in self._courses:
            if course.id == course_id:
                return course
        return None

    def list_all(self):
        return list(self._courses)

    def update(self, course_id: int, title: str) -> Course:
        course = self.get_by_id(course_id)
        if course is None:
            raise ValueError("Course not found")
        course.title = title
        return course

    def delete(self, course_id: int) -> None:
        self._courses = [course for course in self._courses if course.id != course_id]


class FakeEnrollmentRepository:
    def __init__(self) -> None:
        self._enrollments = []
        self._next_id = 1

    def create(self, student_id: int, course_id: int) -> Enrollment:
        enrollment = Enrollment(id=self._next_id, student_id=student_id, course_id=course_id)
        self._next_id += 1
        self._enrollments.append(enrollment)
        return enrollment

    def list_all(self):
        return list(self._enrollments)

    def delete(self, enrollment_id: int) -> None:
        self._enrollments = [enrollment for enrollment in self._enrollments if enrollment.id != enrollment_id]


class StudentServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.student_service = StudentService(FakeStudentRepository())
        self.course_service = CourseService(FakeCourseRepository())
        self.enrollment_service = EnrollmentService(
            FakeEnrollmentRepository(),
            FakeStudentRepository(),
            FakeCourseRepository(),
        )

    def test_create_student_rejects_empty_name(self) -> None:
        with self.assertRaises(ValueError):
            self.student_service.create_student("   ")

    def test_create_student_returns_student(self) -> None:
        student = self.student_service.create_student("Alice")

        self.assertEqual(student.name, "Alice")
        self.assertEqual(student.id, 1)

    def test_create_course_rejects_empty_title(self) -> None:
        with self.assertRaises(ValueError):
            self.course_service.create_course("   ")

    def test_enroll_student_requires_existing_student_and_course(self) -> None:
        with self.assertRaises(ValueError):
            self.enrollment_service.enroll_student(1, 1)


class StudentControllerTests(unittest.TestCase):
    def test_controller_run_prints_records(self) -> None:
        student_repo = FakeStudentRepository()
        course_repo = FakeCourseRepository()
        enrollment_repo = FakeEnrollmentRepository()

        student_service = StudentService(student_repo)
        course_service = CourseService(course_repo)
        enrollment_service = EnrollmentService(enrollment_repo, student_repo, course_repo)
        controller = StudentController(student_service, course_service, enrollment_service)

        output = io.StringIO()
        with redirect_stdout(output):
            controller.run()

        rendered = output.getvalue()
        self.assertIn("Student Database", rendered)
        self.assertIn("Students:", rendered)
        self.assertIn("Courses:", rendered)
        self.assertIn("Enrollments:", rendered)


if __name__ == "__main__":
    unittest.main()
