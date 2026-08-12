const API_BASE_URL = "/api";

async function request(path, options = {}) {
  const headers = {
    "Accept": "application/json",
    ...(options.headers ?? {}),
  };

  const config = {
    ...options,
    headers,
  };

  if (options.body !== undefined && !(options.body instanceof FormData)) {
    config.body = JSON.stringify(options.body);
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(`${API_BASE_URL}${path}`, config);
  const contentType = response.headers.get("Content-Type") || "";
  const bodyText = await response.text();

  let payload = null;
  if (contentType.includes("application/json") && bodyText) {
    payload = JSON.parse(bodyText);
  }

  if (!response.ok) {
    const message = payload?.message || payload?.error || response.statusText || "Request failed";
    const error = new Error(message);
    error.status = response.status;
    error.payload = payload;
    throw error;
  }

  return payload;
}

export async function listStudents() {
  return request("/students", { method: "GET" });
}

export async function createStudent(name) {
  return request("/students", { method: "POST", body: { name } });
}

export async function getStudent(id) {
  return request(`/students/${id}`, { method: "GET" });
}

export async function updateStudent(id, name) {
  return request(`/students/${id}`, { method: "PUT", body: { name } });
}

export async function deleteStudent(id) {
  return request(`/students/${id}`, { method: "DELETE" });
}

export async function listCourses() {
  return request("/courses", { method: "GET" });
}

export async function createCourse(title) {
  return request("/courses", { method: "POST", body: { title } });
}

export async function getCourse(id) {
  return request(`/courses/${id}`, { method: "GET" });
}

export async function updateCourse(id, title) {
  return request(`/courses/${id}`, { method: "PUT", body: { title } });
}

export async function deleteCourse(id) {
  return request(`/courses/${id}`, { method: "DELETE" });
}

export async function listEnrollments() {
  return request("/enrollments", { method: "GET" });
}

export async function createEnrollment(student_id, course_id) {
  return request("/enrollments", { method: "POST", body: { student_id, course_id } });
}

export async function deleteEnrollment(id) {
  return request(`/enrollments/${id}`, { method: "DELETE" });
}
