# ToDoList Capstone Project

A full-stack capstone project built with FastAPI, SQLAlchemy, and Jinja templates for managing personal tasks. The application includes user authentication, protected todo operations, and an admin view for managing application data.

This project is intended as a learning-focused, portfolio-style application rather than a production-ready system. It demonstrates backend API design, database modeling, authentication flow, template rendering, and testing in a real-world CRUD workflow.

## Project Overview

The app allows users to:
- create an account and log in securely
- create, update, delete, and view todo items
- organize tasks with titles, descriptions, priority, and completion status
- access a protected todo dashboard through cookie-based JWT authentication
- view admin-only user and todo listings when assigned the admin role

## Tech Stack

- Python 3.12+
- FastAPI
- SQLAlchemy
- PostgreSQL connection configuration via environment variables
- Jinja2 templates for HTML pages
- JWT-based authentication with cookies
- Pytest for automated tests
- Alembic for database migration support

## Architecture

The project follows a simple layered structure:

- `src/main.py` — FastAPI application startup and route registration
- `src/backend/routers/` — API and page endpoints
- `src/backend/services/` — business logic for auth, todos, users, and admin access
- `src/backend/schema.py` — Pydantic request/response models
- `src/database/models.py` — SQLAlchemy ORM models
- `src/database/db_config.py` — database session configuration
- `src/frontend/templates/` — HTML templates for pages such as login, register, todo dashboard, and editing
- `src/frontend/static/` — CSS and JavaScript assets
- `test/` — pytest test files

## Features

### User Features
- User registration with validation for email, username, and password length
- Login using email and password
- JWT token stored in an HTTP-only cookie
- Logout removes the authentication cookie
- Update profile information and password
- Delete user account

### Todo Features
- Create tasks with a title, description, priority (1–5), and completion status
- View all tasks belonging to the logged-in user
- Edit todo items
- Delete todo items
- Restrict access so users can only see their own tasks

### Admin Features
- Admin-only endpoints for listing all users and todos
- User and todo detail access for authorized administrators
- Role-based access checks on privileged routes

## Capstone Context

This project was designed to showcase the following skills:
- backend API development with FastAPI
- database modeling with SQLAlchemy
- authentication and authorization basics
- form handling and template-based UI integration
- testing with pytest
- application flow design from user account creation to todo management

It is intentionally not treated as a production application. It does not include advanced security hardening, deployment automation, infrastructure layering, or enterprise-grade monitoring, scaling, or resilience features.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/TusharJaiswal689/ToDoList.git
cd ToDoList
```

### 2. Create and activate a virtual environment

On Windows:

```powershell
python -m venv todo
.\todo\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root with the values required by the application:

```env
SECRET_KEY=your_secret_key_here
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todo_db
DB_SSLMODE=disable
```

> Note: The project is configured to use environment-based database settings. If you are using a different database or local setup, update the env values accordingly.

### 5. Run the app

From the `src` directory:

```bash
cd src
uvicorn main:app --reload
```

The application should be available at:

- http://127.0.0.1:8000

## Default Routes

The app includes both API endpoints and rendered pages.

### Authentication pages
- `GET /auth/login-page`
- `GET /auth/register-page`

### Todo pages
- `GET /todo/todo-page`
- `GET /todo/add-todo-page`
- `GET /todo/edit-todo-page/{todo_id}`

### API endpoints
- `POST /auth/token` — login and generate token
- `POST /auth/logout` — log out and clear cookie
- `POST /user/add` — register a user
- `GET /user/me` — fetch current user
- `PUT /user/me` — update user profile
- `PUT /user/me/password` — change password
- `DELETE /user/me` — delete current user
- `GET /todo/me` — list current user's todos
- `POST /todo/add` — create todo
- `PUT /todo/update/{todo_id}` — update todo
- `DELETE /todo/delete/{todo_id}` — delete todo
- `GET /admin/user` — admin list users
- `GET /admin/todo` — admin list todos

## Testing

The project includes Pytest-based tests for key flows such as health checks, authentication behavior, and redirect logic.

Run the full test suite:

```bash
pytest
```

Or run a specific file:

```bash
pytest test/test_main.py
```

## Database and Migrations

Database models are defined in `src/database/models.py`, and Alembic is included for migration management.

Common commands:

```bash
alembic revision -m "description"
alembic upgrade head
```

## Folder Structure

```text
ToDoList/
├── alembic/
├── src/
│   ├── backend/
│   ├── database/
│   ├── frontend/
│   ├── config.py
│   └── main.py
├── test/
├── .env
├── alembic.ini
├── requirements.txt
├── README.md
└── todo/   # local virtual environment
```

## Known Limitations

This is not a production-grade deployment and intentionally omits several operational safeguards, including:
- advanced rate limiting and brute-force protection
- robust logging and monitoring
- environment-specific deployment configuration
- containerization and orchestration
- CI/CD pipeline setup
- production database hardening
- full security auditing and penetration testing

## Future Improvements

Possible next steps for this project include:
- adding task categories or due dates
- implementing admin approval flows and role management
- improving frontend interactivity with a React or JavaScript-heavy UI
- adding password reset and email verification
- adding proper Docker support and deployment workflow
- improving error handling and validation coverage
- expanding test coverage for auth and CRUD operations

## License

This project is for educational and portfolio use. It is not intended for deployment in a production environment without additional review and hardening.

## Acknowledgements

This project demonstrates a student-style capstone implementation of a task management application using the FastAPI ecosystem and common backend patterns.
