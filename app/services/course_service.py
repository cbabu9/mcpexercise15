from typing import List

from app.models.course import Course
from app.repositories.course_repository import CourseRepository


class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    def create_course(self, title: str) -> Course:
        normalized_title = self._normalize_title(title)
        return self.repository.create(normalized_title)

    def list_courses(self) -> List[Course]:
        return self.repository.list_all()

    def update_course(self, course_id: int, title: str) -> Course:
        normalized_title = self._normalize_title(title)
        return self.repository.update(course_id, normalized_title)

    def delete_course(self, course_id: int) -> None:
        self.repository.delete(course_id)

    def _normalize_title(self, title: str) -> str:
        normalized_title = (title or "").strip()
        if not normalized_title:
            raise ValueError("Course title cannot be empty")
        return normalized_title
