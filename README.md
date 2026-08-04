# Student Database Project

This project demonstrates a layered Python architecture for managing students, courses, and enrollments.

## Structure
- app/controllers: CLI controllers
- app/services: business logic
- app/repositories: database access
- app/models: data models
- app/database.py: SQLite initialization

## Database SQL scripts
- Schema: [sql/init_schema.sql](sql/init_schema.sql)
- Sample data: [sql/sample_data.sql](sql/sample_data.sql)

The application loads these scripts automatically during initialization.

## DBHub integration
Set the following environment variables to point the app at a DBHub-style configuration:
```bash
export STUDENT_DB_USE_DBHUB=true
export STUDENT_DB_CONNECTION_STRING="dbhub://your-database"
export STUDENT_DB_PATH="/tmp/student_database.db"
```
If DBHub is not configured, the app falls back to a local SQLite database file.

## REST API usage
The project now exposes a lightweight API layer via [app/api.py](app/api.py) for student, course, and enrollment CRUD operations.

Example usage in Python:
```python
from app.api import StudentApi

api = StudentApi()
print(api.create_student({"name": "Ava"}))
print(api.list_students())
```

## Run tests
```bash
python3 -m unittest discover -s tests -v
```

## Run the app
```bash
python3 -m app.main
```
