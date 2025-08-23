# WoofZoo - FastAPI Clean Architecture Project

A modern FastAPI project following clean architecture principles with layered design, dependency injection, and PostgreSQL database integration.

## 🚀 Features

- **FastAPI** with Python 3.13
- **Clean Architecture** with layered design (Model → Repository → Service → Controller)
- **PostgreSQL** database with SQLAlchemy ORM
- **Dependency Injection** using FastAPI's built-in DI container
- **Alembic** for database migrations
- **Pydantic** for data validation and serialization
- **Comprehensive testing** with pytest
- **Type hints** throughout the codebase
- **Modern Python tooling** (Black, isort, mypy, flake8)

## 📁 Project Structure

```
woofzoo/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection and session management
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── task.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   └── task.py
│   ├── repositories/           # Data access layer
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── task.py
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   └── task.py
│   ├── controllers/            # API controllers
│   │   ├── __init__.py
│   │   └── task.py
│   └── routes/                 # API routes
│       ├── __init__.py
│       └── task.py
├── alembic/                    # Database migrations
├── tests/                      # Test suite
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 🛠️ Setup

### Prerequisites

- Python 3.13+
- PostgreSQL database
- pip or poetry

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd woofzoo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🗄️ Database Setup

1. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE woofzoo;
   ```

2. **Update `.env` file with your database credentials**
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/woofzoo
   ```

3. **Run migrations**
   ```bash
   alembic upgrade head
   ```

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## 🧪 Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_task.py
```

## 🔧 Development Tools

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Type checking
mypy app/

# Linting
flake8 app/ tests/
```

## 📖 API Endpoints

### Tasks CRUD Operations

- `GET /api/tasks` - List all tasks
- `GET /api/tasks/{task_id}` - Get a specific task
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task

### Example Usage

```bash
# Create a task
curl -X POST "http://localhost:8000/api/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "description": "Study clean architecture"}'

# Get all tasks
curl "http://localhost:8000/api/tasks"

# Update a task
curl -X PUT "http://localhost:8000/api/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "description": "Study clean architecture", "completed": true}'
```

## 🏗️ Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

1. **Models** - SQLAlchemy ORM models representing database entities
2. **Schemas** - Pydantic models for request/response validation
3. **Repositories** - Data access layer with database operations
4. **Services** - Business logic layer with domain operations
5. **Controllers** - API layer handling HTTP requests/responses
6. **Routes** - URL routing and endpoint definitions

### Dependency Injection

The project uses FastAPI's dependency injection system to manage dependencies:

```python
# Example dependency injection
def get_task_service() -> TaskService:
    return TaskService(get_task_repository())

@router.get("/tasks")
async def get_tasks(service: TaskService = Depends(get_task_service)):
    return await service.get_all_tasks()
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
