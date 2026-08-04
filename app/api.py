from typing import Any, Dict

from app.database import DatabaseManager
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.student_repository import StudentRepository
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.services.student_service import StudentService


class ApiError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class StudentApi:
    def __init__(self) -> None:
        DatabaseManager.initialize()
        student_repository = StudentRepository()
        course_repository = CourseRepository()
        enrollment_repository = EnrollmentRepository()

        self.student_service = StudentService(student_repository)
        self.course_service = CourseService(course_repository)
        self.enrollment_service = EnrollmentService(enrollment_repository, student_repository, course_repository)

    def create_student(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            name = payload.get("name", "").strip()
            student = self.student_service.create_student(name)
            return {"id": student.id, "name": student.name}
        except ValueError as exc:
            raise ApiError(str(exc), 400) from exc

    def list_students(self) -> Dict[str, Any]:
        students = self.student_service.list_students()
        return {"students": [{"id": item.id, "name": item.name} for item in students]}

    def get_student(self, student_id: int) -> Dict[str, Any]:
        student = self.student_service.repository.get_by_id(student_id)
        if student is None:
            raise ApiError("Student not found", 404)
        return {"id": student.id, "name": student.name}

    def update_student(self, student_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            student = self.student_service.repository.get_by_id(student_id)
            if student is None:
                raise ApiError("Student not found", 404)
            updated_student = self.student_service.update_student(student_id, payload.get("name", ""))
            return {"id": updated_student.id, "name": updated_student.name}
        except ValueError as exc:
            raise ApiError(str(exc), 400) from exc

    def delete_student(self, student_id: int) -> Dict[str, Any]:
        student = self.student_service.repository.get_by_id(student_id)
        if student is None:
            raise ApiError("Student not found", 404)
        self.student_service.delete_student(student_id)
        return {"message": "Student deleted"}

    def create_course(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            title = payload.get("title", "").strip()
            course = self.course_service.create_course(title)
            return {"id": course.id, "title": course.title}
        except ValueError as exc:
            raise ApiError(str(exc), 400) from exc

    def list_courses(self) -> Dict[str, Any]:
        courses = self.course_service.list_courses()
        return {"courses": [{"id": item.id, "title": item.title} for item in courses]}

    def get_course(self, course_id: int) -> Dict[str, Any]:
        course = self.course_service.repository.get_by_id(course_id)
        if course is None:
            raise ApiError("Course not found", 404)
        return {"id": course.id, "title": course.title}

    def update_course(self, course_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            course = self.course_service.repository.get_by_id(course_id)
            if course is None:
                raise ApiError("Course not found", 404)
            updated_course = self.course_service.update_course(course_id, payload.get("title", ""))
            return {"id": updated_course.id, "title": updated_course.title}
        except ValueError as exc:
            raise ApiError(str(exc), 400) from exc

    def delete_course(self, course_id: int) -> Dict[str, Any]:
        course = self.course_service.repository.get_by_id(course_id)
        if course is None:
            raise ApiError("Course not found", 404)
        self.course_service.delete_course(course_id)
        return {"message": "Course deleted"}

    def create_enrollment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        student_id = payload.get("student_id")
        course_id = payload.get("course_id")
        if not isinstance(student_id, int) or not isinstance(course_id, int):
            raise ApiError("student_id and course_id must be integers", 400)
        try:
            enrollment = self.enrollment_service.enroll_student(student_id, course_id)
            return {"id": enrollment.id, "student_id": enrollment.student_id, "course_id": enrollment.course_id}
        except ValueError as exc:
            raise ApiError(str(exc), 400) from exc

    def list_enrollments(self) -> Dict[str, Any]:
        enrollments = self.enrollment_service.list_enrollments()
        return {"enrollments": [{"id": item.id, "student_id": item.student_id, "course_id": item.course_id} for item in enrollments]}

    def delete_enrollment(self, enrollment_id: int) -> Dict[str, Any]:
        self.enrollment_service.enrollment_repository.delete(enrollment_id)
        return {"message": "Enrollment deleted"}
