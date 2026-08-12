import json
import os
import pathlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from app.api import ApiError, StudentApi

HERE = pathlib.Path(__file__).resolve()
FRONTEND_DIR = HERE.parent.parent / "frontend"
API = StudentApi()


def parse_json_request(handler: SimpleHTTPRequestHandler) -> Any:
    if handler.headers.get("Content-Length") is None:
        return None

    length = int(handler.headers["Content-Length"])
    if length == 0:
        return None

    body = handler.rfile.read(length).decode("utf-8")
    if not body:
        return None

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise ApiError("Invalid JSON payload", 400) from exc


class StudentApiHandler(SimpleHTTPRequestHandler):
    api = API

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api("GET", parsed.path)
        else:
            if parsed.path == "/":
                self.path = "/index.html"
            return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api("POST", parsed.path)
        else:
            self.send_error(404)

    def do_PUT(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api("PUT", parsed.path)
        else:
            self.send_error(404)

    def do_DELETE(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            self.handle_api("DELETE", parsed.path)
        else:
            self.send_error(404)

    def handle_api(self, method: str, path: str) -> None:
        try:
            payload = parse_json_request(self) if method in {"POST", "PUT"} else None
            response, status = self.route_api(method, path, payload)
            self.respond_json(response, status)
        except ApiError as exc:
            self.respond_json({"error": exc.message}, exc.status_code)
        except Exception as exc:
            import traceback

            traceback.print_exc()
            self.respond_json({"error": "Internal server error"}, 500)

    def route_api(self, method: str, path: str, payload: Any | None) -> tuple[dict[str, Any], int]:
        parts = path[len("/api"):].strip("/").split("/")
        if parts[0] == "students":
            return self.route_students(method, parts[1:] if len(parts) > 1 else [], payload)
        if parts[0] == "courses":
            return self.route_courses(method, parts[1:] if len(parts) > 1 else [], payload)
        if parts[0] == "enrollments":
            return self.route_enrollments(method, parts[1:] if len(parts) > 1 else [], payload)
        return {"error": "Endpoint not found"}, 404

    def route_students(self, method: str, segments: list[str], payload: Any | None) -> tuple[dict[str, Any], int]:
        if method == "GET" and not segments:
            return self.api.list_students(), 200
        if method == "POST" and not segments:
            return self.api.create_student(payload or {}), 201
        if len(segments) == 1 and segments[0].isdigit():
            student_id = int(segments[0])
            if method == "GET":
                return self.api.get_student(student_id), 200
            if method == "PUT":
                return self.api.update_student(student_id, payload or {}), 200
            if method == "DELETE":
                return self.api.delete_student(student_id), 200
        return {"error": "Student endpoint not found"}, 404

    def route_courses(self, method: str, segments: list[str], payload: Any | None) -> tuple[dict[str, Any], int]:
        if method == "GET" and not segments:
            return self.api.list_courses(), 200
        if method == "POST" and not segments:
            return self.api.create_course(payload or {}), 201
        if len(segments) == 1 and segments[0].isdigit():
            course_id = int(segments[0])
            if method == "GET":
                return self.api.get_course(course_id), 200
            if method == "PUT":
                return self.api.update_course(course_id, payload or {}), 200
            if method == "DELETE":
                return self.api.delete_course(course_id), 200
        return {"error": "Course endpoint not found"}, 404

    def route_enrollments(self, method: str, segments: list[str], payload: Any | None) -> tuple[dict[str, Any], int]:
        if method == "GET" and not segments:
            return self.api.list_enrollments(), 200
        if method == "POST" and not segments:
            return self.api.create_enrollment(payload or {}), 201
        if len(segments) == 1 and segments[0].isdigit() and method == "DELETE":
            return self.api.delete_enrollment(int(segments[0])), 200
        return {"error": "Enrollment endpoint not found"}, 404

    def respond_json(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run(server_address: tuple[str, int] = ("127.0.0.1", 8000)) -> None:
    print(f"Starting server at http://{server_address[0]}:{server_address[1]}")
    with ThreadingHTTPServer(server_address, StudentApiHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    run()
