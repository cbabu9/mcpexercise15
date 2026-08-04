from typing import List

from app.models.enrollment import Enrollment
from app.repositories.base_repository import BaseRepository


class EnrollmentRepository(BaseRepository):
    def create(self, student_id: int, course_id: int) -> Enrollment:
        cursor = self._connect().execute(
            "INSERT INTO enrollments(student_id, course_id) VALUES (?, ?)",
            (student_id, course_id),
        )
        self._connect().commit()
        return Enrollment(id=cursor.lastrowid, student_id=student_id, course_id=course_id)

    def list_all(self) -> List[Enrollment]:
        rows = self._connect().execute("SELECT id, student_id, course_id FROM enrollments ORDER BY id").fetchall()
        return [Enrollment(id=row[0], student_id=row[1], course_id=row[2]) for row in rows]

    def delete(self, enrollment_id: int) -> None:
        self._connect().execute("DELETE FROM enrollments WHERE id = ?", (enrollment_id,))
        self._connect().commit()
