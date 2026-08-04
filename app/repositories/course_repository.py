from typing import List, Optional

from app.models.course import Course
from app.repositories.base_repository import BaseRepository


class CourseRepository(BaseRepository):
    def create(self, title: str) -> Course:
        code = "".join(ch for ch in title.upper() if ch.isalnum())[:8] or "COURSE"
        cursor = self._connect().execute(
            "INSERT INTO courses(title, code) VALUES (?, ?)",
            (title, code),
        )
        self._connect().commit()
        course_id = cursor.lastrowid
        return Course(id=course_id, title=title)

    def get_by_id(self, course_id: int) -> Optional[Course]:
        row = self._connect().execute("SELECT id, title FROM courses WHERE id = ?", (course_id,)).fetchone()
        return Course(id=row[0], title=row[1]) if row else None

    def list_all(self) -> List[Course]:
        rows = self._connect().execute("SELECT id, title FROM courses ORDER BY id").fetchall()
        return [Course(id=row[0], title=row[1]) for row in rows]

    def update(self, course_id: int, title: str) -> Course:
        self._connect().execute("UPDATE courses SET title = ? WHERE id = ?", (title, course_id))
        self._connect().commit()
        return Course(id=course_id, title=title)

    def delete(self, course_id: int) -> None:
        self._connect().execute("DELETE FROM courses WHERE id = ?", (course_id,))
        self._connect().commit()
