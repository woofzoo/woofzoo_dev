#!/bin/bash

# WoofZoo FastAPI Project - Quick Start Script

set -e

echo "🚀 Starting WoofZoo FastAPI Project Setup..."

# Check if Python 3.13+ is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.13"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.13 or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp env.example .env
    echo "📝 Please edit .env file with your database credentials"
fi

# Check if PostgreSQL is running (optional)
if command -v pg_isready &> /dev/null; then
    if pg_isready -q; then
        echo "✅ PostgreSQL is running"
    else
        echo "⚠️ PostgreSQL is not running. You can start it with:"
        echo "   brew services start postgresql  # macOS"
        echo "   sudo systemctl start postgresql  # Linux"
        echo "   Or use Docker: docker-compose up -d postgres"
    fi
fi

# Run database migrations if Alembic is set up
if [ -f "alembic.ini" ]; then
    echo "🗄️ Running database migrations..."
    alembic upgrade head || echo "⚠️ Migration failed. Make sure your database is running and configured."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the development server:"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "Or use the Makefile:"
echo "   make run"
echo ""
echo "📚 API Documentation will be available at:"
echo "   http://localhost:8000/docs"
echo ""
echo "🧪 To run tests:"
echo "   make test"
echo ""
echo "🔧 For more commands, run:"
echo "   make help"
