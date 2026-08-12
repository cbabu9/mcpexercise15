import * as api from "./services/apiService.js";
import {
  createActionButton,
  createCell,
  populateSelectOptions,
} from "./components/uiHelpers.js";
import {
  renderEnrollmentRow,
  renderStudentRow,
  renderCourseRow,
  renderTableRows,
} from "./components/tableComponent.js";

const statusEl = document.getElementById("status");
const studentForm = document.getElementById("create-student-form");
const courseForm = document.getElementById("create-course-form");
const enrollmentForm = document.getElementById("create-enrollment-form");
const studentNameInput = document.getElementById("student-name");
const courseTitleInput = document.getElementById("course-title");
const studentSelect = document.getElementById("enrollment-student");
const courseSelect = document.getElementById("enrollment-course");
const studentsTableBody = document.querySelector("#students-table tbody");
const coursesTableBody = document.querySelector("#courses-table tbody");
const enrollmentsTableBody = document.querySelector("#enrollments-table tbody");

let loadingCounter = 0;

function setStatus(message, options = {}) {
  const { isError = false, hidden = false } = options;
  statusEl.textContent = message;
  statusEl.className = hidden ? "hidden" : isError ? "error" : "";
}

function beginLoading() {
  loadingCounter += 1;
  if (loadingCounter === 1) {
    setStatus("Loading…", { hidden: false });
  }
}

function endLoading() {
  loadingCounter = Math.max(0, loadingCounter - 1);
  if (loadingCounter === 0) {
    setStatus("Ready", { hidden: false });
  }
}

async function loadAllData() {
  beginLoading();
  try {
    const [studentsResponse, coursesResponse, enrollmentsResponse] = await Promise.all([
      api.listStudents(),
      api.listCourses(),
      api.listEnrollments(),
    ]);

    renderStudents(studentsResponse.students || []);
    renderCourses(coursesResponse.courses || []);
    renderEnrollments(enrollmentsResponse.enrollments || [], studentsResponse.students || [], coursesResponse.courses || []);
    populateEnrollmentOptions(studentsResponse.students || [], coursesResponse.courses || []);
    setStatus("Ready");
  } catch (error) {
    setStatus(error.message || "Unable to load data", { isError: true });
  } finally {
    endLoading();
  }
}

function renderStudents(students) {
  renderTableRows(studentsTableBody, students, (row, student) => {
    renderStudentRow(row, student, promptUpdateStudent, confirmDeleteStudent);
  });
}

function renderCourses(courses) {
  renderTableRows(coursesTableBody, courses, (row, course) => {
    renderCourseRow(row, course, promptUpdateCourse, confirmDeleteCourse);
  });
}

function renderEnrollments(enrollments, students, courses) {
  renderTableRows(enrollmentsTableBody, enrollments, (row, enrollment) => {
    renderEnrollmentRow(row, enrollment, students, courses, confirmDeleteEnrollment);
  });
}

function populateEnrollmentOptions(students, courses) {
  populateSelectOptions(studentSelect, students, (student) => `${student.name} (#${student.id})`);
  populateSelectOptions(courseSelect, courses, (course) => `${course.title} (#${course.id})`);
}

async function handleStudentSubmit(event) {
  event.preventDefault();
  const name = studentNameInput.value.trim();
  if (!name) {
    setStatus("Student name cannot be empty", { isError: true });
    return;
  }

  beginLoading();
  try {
    await api.createStudent(name);
    studentNameInput.value = "";
    await loadAllData();
    setStatus("Student created successfully");
  } catch (error) {
    setStatus(error.message || "Unable to create student", { isError: true });
  } finally {
    endLoading();
  }
}

async function handleCourseSubmit(event) {
  event.preventDefault();
  const title = courseTitleInput.value.trim();
  if (!title) {
    setStatus("Course title cannot be empty", { isError: true });
    return;
  }

  beginLoading();
  try {
    await api.createCourse(title);
    courseTitleInput.value = "";
    await loadAllData();
    setStatus("Course created successfully");
  } catch (error) {
    setStatus(error.message || "Unable to create course", { isError: true });
  } finally {
    endLoading();
  }
}

async function handleEnrollmentSubmit(event) {
  event.preventDefault();
  const studentId = Number(studentSelect.value);
  const courseId = Number(courseSelect.value);
  if (!studentId || !courseId) {
    setStatus("Please select both a student and a course", { isError: true });
    return;
  }

  beginLoading();
  try {
    await api.createEnrollment(studentId, courseId);
    studentSelect.value = "";
    courseSelect.value = "";
    await loadAllData();
    setStatus("Student enrolled successfully");
  } catch (error) {
    setStatus(error.message || "Unable to create enrollment", { isError: true });
  } finally {
    endLoading();
  }
}

async function promptUpdateStudent(student) {
  const name = window.prompt("Update student name:", student.name);
  if (name === null) {
    return;
  }

  const trimmed = name.trim();
  if (!trimmed) {
    setStatus("Student name cannot be empty", { isError: true });
    return;
  }

  beginLoading();
  try {
    await api.updateStudent(student.id, trimmed);
    await loadAllData();
    setStatus("Student updated successfully");
  } catch (error) {
    setStatus(error.message || "Unable to update student", { isError: true });
  } finally {
    endLoading();
  }
}

async function promptUpdateCourse(course) {
  const title = window.prompt("Update course title:", course.title);
  if (title === null) {
    return;
  }

  const trimmed = title.trim();
  if (!trimmed) {
    setStatus("Course title cannot be empty", { isError: true });
    return;
  }

  beginLoading();
  try {
    await api.updateCourse(course.id, trimmed);
    await loadAllData();
    setStatus("Course updated successfully");
  } catch (error) {
    setStatus(error.message || "Unable to update course", { isError: true });
  } finally {
    endLoading();
  }
}

async function confirmDeleteStudent(studentId) {
  if (!window.confirm("Delete this student?")) {
    return;
  }

  beginLoading();
  try {
    await api.deleteStudent(studentId);
    await loadAllData();
    setStatus("Student deleted successfully");
  } catch (error) {
    setStatus(error.message || "Unable to delete student", { isError: true });
  } finally {
    endLoading();
  }
}

async function confirmDeleteCourse(courseId) {
  if (!window.confirm("Delete this course?")) {
    return;
  }

  beginLoading();
  try {
    await api.deleteCourse(courseId);
    await loadAllData();
    setStatus("Course deleted successfully");
  } catch (error) {
    setStatus(error.message || "Unable to delete course", { isError: true });
  } finally {
    endLoading();
  }
}

async function confirmDeleteEnrollment(enrollmentId) {
  if (!window.confirm("Delete this enrollment?")) {
    return;
  }

  beginLoading();
  try {
    await api.deleteEnrollment(enrollmentId);
    await loadAllData();
    setStatus("Enrollment deleted successfully");
  } catch (error) {
    setStatus(error.message || "Unable to delete enrollment", { isError: true });
  } finally {
    endLoading();
  }
}

studentForm.addEventListener("submit", handleStudentSubmit);
courseForm.addEventListener("submit", handleCourseSubmit);
enrollmentForm.addEventListener("submit", handleEnrollmentSubmit);

window.addEventListener("DOMContentLoaded", () => {
  setStatus("Ready", { hidden: false });
  loadAllData();
});
