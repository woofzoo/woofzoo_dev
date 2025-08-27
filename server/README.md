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
│   │   └── user.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── repositories/           # Data access layer
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── user.py
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── email.py
│   │   └── jwt.py
│   ├── controllers/            # API controllers
│   │   ├── __init__.py
│   │   └── auth.py
│   └── routes/                 # API routes
│       ├── __init__.py
│       └── auth.py
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
pytest tests/test_auth.py
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

### Authentication Operations

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/verify-email` - Verify user email
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password

### Example Usage

```bash
# Register a new user
curl -X POST "http://localhost:8000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123", "full_name": "John Doe"}'

# Login user
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123"}'

# Refresh token
curl -X POST "http://localhost:8000/api/auth/refresh" \
     -H "Content-Type: application/json" \
     -d '{"refresh_token": "your_refresh_token"}'
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
def get_auth_service() -> AuthService:
    return AuthService(get_user_repository(), get_email_service(), get_jwt_service())

@router.post("/auth/login")
def login(service: AuthService = Depends(get_auth_service)):
    return service.login_user(login_data)
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
