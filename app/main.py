from app.config import load_database_config
from app.controllers.student_controller import StudentController
from app.database import DatabaseManager
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.student_repository import StudentRepository
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.services.student_service import StudentService


def main() -> None:
    config = load_database_config()
    print(f"Database backend: {'DBHub' if config.use_dbhub else 'SQLite'}")
    DatabaseManager.initialize()
    student_repository = StudentRepository()
    course_repository = CourseRepository()
    enrollment_repository = EnrollmentRepository()

    student_service = StudentService(student_repository)
    course_service = CourseService(course_repository)
    enrollment_service = EnrollmentService(enrollment_repository, student_repository, course_repository)

    controller = StudentController(student_service, course_service, enrollment_service)
    controller.run()


if __name__ == "__main__":
    main()
