from typing import List

from app.models.enrollment import Enrollment
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.student_repository import StudentRepository


class EnrollmentService:
    def __init__(self, enrollment_repository: EnrollmentRepository, student_repository: StudentRepository, course_repository: CourseRepository):
        self.enrollment_repository = enrollment_repository
        self.student_repository = student_repository
        self.course_repository = course_repository

    def enroll_student(self, student_id: int, course_id: int) -> Enrollment:
        if self.student_repository.get_by_id(student_id) is None:
            raise ValueError("Student does not exist")
        if self.course_repository.get_by_id(course_id) is None:
            raise ValueError("Course does not exist")
        return self.enrollment_repository.create(student_id, course_id)

    def list_enrollments(self) -> List[Enrollment]:
        return self.enrollment_repository.list_all()
