import { createCell, createActionButton, clearChildren } from "./uiHelpers.js";

export function renderTableRows(bodyElement, items, renderRow) {
  clearChildren(bodyElement);
  items.forEach((item) => {
    const row = document.createElement("tr");
    renderRow(row, item);
    bodyElement.appendChild(row);
  });
}

export function renderStudentRow(row, student, onEdit, onDelete) {
  row.appendChild(createCell(student.id));
  row.appendChild(createCell(student.name));

  const actionsCell = document.createElement("td");
  actionsCell.appendChild(createActionButton("Edit", "primary", () => onEdit(student)));
  actionsCell.appendChild(createActionButton("Delete", "danger", () => onDelete(student.id)));
  row.appendChild(actionsCell);
}

export function renderCourseRow(row, course, onEdit, onDelete) {
  row.appendChild(createCell(course.id));
  row.appendChild(createCell(course.title));

  const actionsCell = document.createElement("td");
  actionsCell.appendChild(createActionButton("Edit", "primary", () => onEdit(course)));
  actionsCell.appendChild(createActionButton("Delete", "danger", () => onDelete(course.id)));
  row.appendChild(actionsCell);
}

export function renderEnrollmentRow(row, enrollment, students, courses, onDelete) {
  const student = students.find((item) => item.id === enrollment.student_id);
  const course = courses.find((item) => item.id === enrollment.course_id);

  row.appendChild(createCell(enrollment.id));
  row.appendChild(createCell(student?.name || `ID ${enrollment.student_id}`));
  row.appendChild(createCell(course?.title || `ID ${enrollment.course_id}`));

  const actionsCell = document.createElement("td");
  actionsCell.appendChild(createActionButton("Delete", "danger", () => onDelete(enrollment.id)));
  row.appendChild(actionsCell);
}
