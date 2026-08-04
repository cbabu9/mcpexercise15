from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.services.student_service import StudentService


class StudentController:
    def __init__(self, student_service: StudentService, course_service: CourseService, enrollment_service: EnrollmentService):
        self.student_service = student_service
        self.course_service = course_service
        self.enrollment_service = enrollment_service

    def run(self) -> None:
        print("Student Database")
        student = self.student_service.create_student("Alice")
        course = self.course_service.create_course("Physics")
        self.enrollment_service.enroll_student(student.id, course.id)

        print("Students:")
        for item in self.student_service.list_students():
            print(f"- {item.id}: {item.name}")

        print("Courses:")
        for item in self.course_service.list_courses():
            print(f"- {item.id}: {item.title}")

        print("Enrollments:")
        for item in self.enrollment_service.list_enrollments():
            print(f"- {item.id}: student {item.student_id} -> course {item.course_id}")
