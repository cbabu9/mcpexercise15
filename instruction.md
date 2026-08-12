# Project Instructions

## Project purpose
- Build a Python-based student database application with a clear layered architecture.
- Support students, courses, and enrollments through a simple and maintainable design.
- Keep the project easy to extend with additional features such as CRUD operations, APIs, or web interfaces.

## Architecture guidelines
- Follow a layered structure with separate modules for controllers, services, repositories, and models.
- Keep controllers focused on handling input and output only.
- Put business rules in services.
- Keep database access logic inside repositories.
- Use models to represent domain entities and keep them simple data containers.
- Avoid mixing persistence logic into controllers or services.
- Serve frontend static assets through the Python server when adding a web UI.
- Keep API routing and UI rendering concerns separated.

## Frontend guidelines
- Place static UI files in `frontend/`.
- Use a service layer for API calls and to centralize error handling.
- Keep DOM rendering logic in separate helper modules when possible.
- Provide user feedback for loading and error states.

## Coding standards
- Use Python 3 and follow PEP 8 style conventions.
- Write clear, descriptive names for classes, methods, and variables.
- Keep functions focused on a single responsibility.
- Add docstrings to important classes and methods where useful.
- Prefer small, reusable components over large monolithic modules.
- Handle invalid input with clear exceptions or validation messages.

## Database integration rules
- Use SQLite for local development and testing.
- Initialize the database schema in a dedicated database module.
- Keep SQL statements inside repository classes.
- Use parameterized queries to prevent SQL injection.
- Ensure tables for Students, Courses, and Enrollments are created consistently.
- Prefer committing changes explicitly after write operations.

## Testing guidelines
- Write tests for service and repository behavior whenever new features are added.
- Use unittest for project tests.
- Keep tests focused on real behavior rather than implementation details.
- Add tests for both success and error scenarios.
- Run the test suite regularly after changes to verify the application still works.
