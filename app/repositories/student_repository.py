from typing import List, Optional

from app.models.student import Student
from app.repositories.base_repository import BaseRepository


class StudentRepository(BaseRepository):
    def create(self, name: str) -> Student:
        cursor = self._connect().execute("INSERT INTO students(name) VALUES (?)", (name,))
        self._connect().commit()
        student_id = cursor.lastrowid
        return Student(id=student_id, name=name)

    def get_by_id(self, student_id: int) -> Optional[Student]:
        row = self._connect().execute("SELECT id, name FROM students WHERE id = ?", (student_id,)).fetchone()
        return Student(id=row[0], name=row[1]) if row else None

    def list_all(self) -> List[Student]:
        rows = self._connect().execute("SELECT id, name FROM students ORDER BY id").fetchall()
        return [Student(id=row[0], name=row[1]) for row in rows]

    def update(self, student_id: int, name: str) -> Student:
        self._connect().execute("UPDATE students SET name = ? WHERE id = ?", (name, student_id))
        self._connect().commit()
        return Student(id=student_id, name=name)

    def delete(self, student_id: int) -> None:
        self._connect().execute("DELETE FROM students WHERE id = ?", (student_id,))
        self._connect().commit()
