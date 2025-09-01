# Testing Setup Guide

This guide explains how to set up and run tests for the WoofZoo API with different database configurations.

## Overview

The test suite supports multiple database configurations to accommodate different testing needs:

1. **In-Memory SQLite** (Default) - Fastest, no cleanup needed
2. **File-based SQLite** - Persistent, good for debugging
3. **PostgreSQL** - Most realistic, production-like testing

## Quick Start

### 1. Install Dependencies

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Or install all dependencies including test ones
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Run Tests (Default - In-Memory SQLite)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_integration_01_auth.py

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

## Database Configuration Options

### Option 1: In-Memory SQLite (Recommended for Development)

**Pros:**
- Fastest execution
- No cleanup required
- No external dependencies
- Perfect for CI/CD

**Cons:**
- Not production-like
- Limited SQL features

**Usage:**
```bash
# Default - no environment variable needed
pytest

# Or explicitly set
export TEST_DATABASE_URL="sqlite:///:memory:"
pytest
```

### Option 2: File-based SQLite (Good for Debugging)

**Pros:**
- Persistent database for debugging
- Can inspect data between tests
- No external dependencies

**Cons:**
- Slower than in-memory
- Requires cleanup

**Usage:**
```bash
export TEST_DATABASE_URL="sqlite:///./test_woofzoo.db"
pytest

# Clean up after testing
rm -f test_woofzoo.db
```

### Option 3: PostgreSQL (Production-like Testing)

**Pros:**
- Most realistic testing environment
- Full SQL feature support
- Production-like behavior

**Cons:**
- Requires PostgreSQL installation
- Slower setup
- More complex configuration

**Setup:**
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Or using Docker
docker run --name postgres-test -e POSTGRES_PASSWORD=test_pass -e POSTGRES_DB=woofzoo_test -p 5432:5432 -d postgres:13

# Create test database
createdb woofzoo_test

# Set environment variable
export TEST_DATABASE_URL="postgresql://test_user:test_pass@localhost:5432/woofzoo_test"
pytest
```

## Test Configuration

### Environment Variables

Create a `.env.test` file for test-specific configuration:

```bash
# Test Database
TEST_DATABASE_URL=sqlite:///:memory:

# Test Settings
TESTING=true
DEBUG=true
AUTO_VERIFY_USERS=true

# Disable external services for testing
MAILGUN_API_KEY=dummy_key
MSG91_API_KEY=dummy_key
S3_ACCESS_KEY=dummy_key
S3_SECRET_KEY=dummy_key
```

### Test Markers

The test suite uses custom markers for different test types:

```bash
# Run only fast tests
pytest -m "not slow"

# Run only integration tests
pytest -m integration

# Run tests for specific database type
pytest -m sqlite_memory
pytest -m postgres

# Run tests excluding integration
pytest -m "not integration"
```

## Test Structure

### Fixtures

The test suite provides comprehensive fixtures:

- **Database Fixtures**: `db_session`, `test_database`
- **Client Fixtures**: `client`, `authenticated_client`, `admin_client`
- **Data Fixtures**: `sample_user`, `sample_owner`, `sample_pet`, etc.
- **Utility Functions**: `create_test_user()`, `create_test_owner()`

### Test Categories

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test API endpoints with database
3. **End-to-End Tests**: Test complete user workflows

## Running Specific Test Types

### Unit Tests
```bash
# Run unit tests only
pytest tests/unit/

# Run specific unit test
pytest tests/unit/test_auth_service.py
```

### Integration Tests
```bash
# Run integration tests
pytest tests/test_integration_*.py

# Run specific integration test
pytest tests/test_integration_01_auth.py -v
```

### Acceptance Tests
```bash
# Run acceptance tests
pytest tests/acceptance_tests_*.py

# Run specific acceptance test phase
pytest tests/acceptance_tests_01_authentication.py
```

## Test Data Management

### Sample Data

The test suite includes pre-configured sample data:

```python
# Use sample data fixtures
def test_create_pet(client, sample_owner):
    response = client.post("/api/pets/", json={
        "name": "Buddy",
        "owner_id": sample_owner.id,
        # ... other fields
    })
    assert response.status_code == 201
```

### Creating Custom Test Data

```python
# Use utility functions
def test_custom_scenario(db_session):
    user = create_test_user(db_session, email="custom@example.com")
    owner = create_test_owner(db_session, phone="+9876543210")
    # ... test logic
```

## Debugging Tests

### Database Inspection

When using file-based SQLite:

```bash
# After running tests, inspect the database
sqlite3 test_woofzoo.db

# List tables
.tables

# Query data
SELECT * FROM users;
SELECT * FROM pets;
```

### Test Isolation

Each test runs in its own transaction that gets rolled back:

```python
def test_user_creation(db_session):
    # This test starts with a clean database
    user = create_test_user(db_session)
    assert user.email == "test@example.com"
    # Database is automatically cleaned up after test
```

### Debugging Failed Tests

```bash
# Run with maximum verbosity
pytest -vvv tests/test_integration_01_auth.py

# Run specific test with debug output
pytest tests/test_integration_01_auth.py::test_user_registration -s

# Run with database echo
export TEST_DATABASE_URL="sqlite:///./test_woofzoo.db"
pytest --log-cli-level=DEBUG
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          export TEST_DATABASE_URL="sqlite:///:memory:"
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

### Docker Testing

```dockerfile
# Dockerfile for testing
FROM python:3.11-slim

WORKDIR /app
COPY requirements*.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

COPY . .
ENV TEST_DATABASE_URL="sqlite:///:memory:"
ENV TESTING=true

CMD ["pytest", "--cov=app"]
```

## Best Practices

### 1. Test Database Selection

- **Development**: Use in-memory SQLite for speed
- **Debugging**: Use file-based SQLite for inspection
- **CI/CD**: Use in-memory SQLite for reliability
- **Integration Testing**: Use PostgreSQL for realism

### 2. Test Data Management

- Use fixtures for common test data
- Create utility functions for custom scenarios
- Avoid hardcoded test data
- Use realistic but safe test data

### 3. Test Isolation

- Each test should be independent
- Use transaction rollback for cleanup
- Avoid test interdependencies
- Use unique identifiers for test data

### 4. Performance

- Use appropriate database for test type
- Avoid unnecessary database operations
- Use efficient test data creation
- Monitor test execution time

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check database URL
   echo $TEST_DATABASE_URL
   
   # Test database connection
   python -c "from tests.conftest import test_engine; print('DB OK')"
   ```

2. **Import Errors**
   ```bash
   # Check Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   
   # Install missing dependencies
   pip install -r requirements-dev.txt
   ```

3. **Test Failures**
   ```bash
   # Run with more detail
   pytest -vvv --tb=long
   
   # Check test database state
   sqlite3 test_woofzoo.db ".tables"
   ```

### Getting Help

- Check the test logs for detailed error messages
- Use the debugging techniques above
- Review the test configuration in `conftest.py`
- Ensure all dependencies are installed

## Advanced Configuration

### Custom Test Database

Create a custom test configuration:

```python
# tests/custom_conftest.py
import pytest
from tests.conftest import TestConfig

class CustomTestConfig(TestConfig):
    DATABASE_URL = "postgresql://custom_user:custom_pass@localhost:5432/custom_test"
    DEBUG = True
    AUTO_VERIFY_USERS = True

# Use in specific test files
pytest_plugins = ["tests.custom_conftest"]
```

### Parallel Testing

For large test suites, consider parallel execution:

```bash
# Install parallel test runner
pip install pytest-xdist

# Run tests in parallel
pytest -n auto

# Run with specific number of workers
pytest -n 4
```

This setup provides a robust, flexible testing environment that can adapt to different needs while maintaining test reliability and performance.
