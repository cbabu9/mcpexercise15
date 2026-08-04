from dataclasses import dataclass


@dataclass
class Enrollment:
    id: int
    student_id: int
    course_id: int
