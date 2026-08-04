from typing import List

from app.models.student import Student
from app.repositories.student_repository import StudentRepository


class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def create_student(self, name: str) -> Student:
        normalized_name = self._normalize_name(name)
        return self.repository.create(normalized_name)

    def list_students(self) -> List[Student]:
        return self.repository.list_all()

    def update_student(self, student_id: int, name: str) -> Student:
        normalized_name = self._normalize_name(name)
        return self.repository.update(student_id, normalized_name)

    def delete_student(self, student_id: int) -> None:
        self.repository.delete(student_id)

    def _normalize_name(self, name: str) -> str:
        normalized_name = (name or "").strip()
        if not normalized_name:
            raise ValueError("Student name cannot be empty")
        return normalized_name
