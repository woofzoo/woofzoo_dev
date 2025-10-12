# Cursor Rules for WoofZoo Development

## 🐍 Environment Management

### Conda Environment Activation
**ALWAYS** activate the conda environment before running any Python commands, pip install, or package management operations:

```bash
# ✅ CORRECT - Always activate environment first
conda activate woofzoo
pip install -r requirements.txt
python -c "from app.main import app; print('✅ Success')"

# ❌ INCORRECT - Don't run Python commands without activating environment
pip install -r requirements.txt  # This might install to wrong environment
python -c "from app.main import app"  # This might use wrong Python
```

### Environment Setup Commands
```bash
# Create and activate environment
conda create -n woofzoo python=3.13
conda activate woofzoo

# Install dependencies
pip install -r requirements.txt

# Verify environment
python -c "import sys; print(f'Python: {sys.executable}')"
conda list | grep -E "(fastapi|sqlalchemy|pydantic)"
```

### Standard Command Pattern
**ALWAYS** use this pattern for Python commands:

```bash
# ✅ CORRECT - Always activate environment first
conda activate woofzoo && python your_script.py
conda activate woofzoo && pip install package_name
conda activate woofzoo && python -c "from app.main import app"

# For scripts that need PYTHONPATH
conda activate woofzoo && PYTHONPATH=/Users/noname/code/woofzoo_dev/server python examples/test_email_templates.py
```

## 🏗️ Project Structure

### Clean Architecture Layers
Always follow the layered architecture pattern:
```
Routes → Controllers → Services → Repositories → Models
```

### File Organization
- **Models**: Database entities only
- **Schemas**: Data validation and serialization
- **Repositories**: Database operations only
- **Services**: Business logic and rules
- **Controllers**: HTTP handling and error responses
- **Routes**: Endpoint definitions and dependency injection

## 🐛 Common Issues & Solutions

### Environment Issues
1. **Wrong Python Environment**: Always run `conda activate woofzoo` first
2. **Missing Dependencies**: Run `pip install -r requirements.txt` after activating environment
3. **Import Errors**: Check if running from correct directory with correct environment

### Database Issues
1. **Migration Failures**: Ensure database is accessible and has proper permissions
2. **Connection Issues**: Check DATABASE_URL and network connectivity
3. **Alembic Not Found**: Install alembic in the correct environment

### Testing Issues
1. **Module Not Found**: Set PYTHONPATH or run from correct directory
2. **Environment Mismatch**: Ensure test environment matches development environment

## 🚀 Best Practices

### Before Running Commands
1. ✅ Activate conda environment: `conda activate woofzoo`
2. ✅ Check current directory: `pwd` (should be in `/Users/noname/code/woofzoo_dev/server`)
3. ✅ Verify Python environment: `which python`
4. ✅ Install dependencies if needed: `pip install -r requirements.txt`

### Code Quality
1. ✅ Run linting: `make lint` or `black app/`
2. ✅ Check types: `make type-check` or `mypy app/`
3. ✅ Run tests: `make test` or `pytest tests/`
4. ✅ Format code: `make format` or `black app/`

### Git Workflow
1. ✅ Use conventional commit format: `type(scope): description`
2. ✅ Test before committing
3. ✅ Update documentation when adding features

## 📋 Checklist for New Features

### Environment Setup
- [ ] Activate conda environment: `conda activate woofzoo`
- [ ] Install new dependencies: `pip install package_name`
- [ ] Update requirements.txt if needed
- [ ] Test imports work correctly

### Code Implementation
- [ ] Follow Clean Architecture layers
- [ ] Add proper type hints
- [ ] Include docstrings
- [ ] Add error handling
- [ ] Follow naming conventions

### Testing
- [ ] Write unit tests
- [ ] Test API endpoints
- [ ] Verify database operations
- [ ] Check error scenarios

### Documentation
- [ ] Update API documentation
- [ ] Add usage examples
- [ ] Update README if needed
- [ ] Document configuration changes

## 🔧 Development Commands

### Environment Management
```bash
# Activate environment
conda activate woofzoo

# Install dependencies
pip install -r requirements.txt

# Check environment
conda list
python --version
```

### Database Operations
```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"

# Rollback migration
alembic downgrade -1
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/
```

### Code Quality
```bash
# Format code
black app/

# Check types
mypy app/

# Lint code
flake8 app/
```

## 🚨 Important Reminders

1. **ALWAYS** activate conda environment before Python operations
2. **NEVER** commit sensitive data (API keys, passwords)
3. **ALWAYS** test before committing
4. **ALWAYS** follow Clean Architecture principles
5. **ALWAYS** add proper error handling
6. **ALWAYS** include type hints and docstrings

## 📚 Reference Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

**Remember: Environment first, then everything else! 🐍✨**
