#!/bin/bash

# Test Environment Setup Script
# This script sets up the environment for running tests

set -e

echo "🐕 Setting up WoofZoo Test Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Python found: $PYTHON_VERSION"
    else
        print_error "Python 3 is not installed. Please install Python 3.8+"
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        print_success "pip found"
    else
        print_error "pip is not installed. Please install pip"
        exit 1
    fi
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Install base requirements
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
        print_success "Base requirements installed"
    else
        print_warning "requirements.txt not found"
    fi
    
    # Install test requirements
    if [ -f "requirements-dev.txt" ]; then
        pip3 install -r requirements-dev.txt
        print_success "Test requirements installed"
    else
        print_warning "requirements-dev.txt not found, installing basic test packages"
        pip3 install pytest pytest-asyncio pytest-cov httpx
    fi
}

# Setup test database
setup_test_database() {
    print_status "Setting up test database..."
    
    # Check if PostgreSQL is available for testing
    if command -v psql &> /dev/null; then
        print_status "PostgreSQL found. Setting up test database..."
        
        # Create test database if it doesn't exist
        if ! psql -lqt | cut -d \| -f 1 | grep -qw woofzoo_test; then
            print_status "Creating test database 'woofzoo_test'..."
            createdb woofzoo_test
            print_success "Test database created"
        else
            print_success "Test database already exists"
        fi
        
        # Set environment variable for PostgreSQL
        export TEST_DATABASE_URL="postgresql://postgres@localhost:5432/woofzoo_test"
        print_success "PostgreSQL test database configured"
    else
        print_status "PostgreSQL not found, using SQLite for testing"
        export TEST_DATABASE_URL="sqlite:///:memory:"
        print_success "SQLite test database configured"
    fi
}

# Setup test environment variables
setup_environment() {
    print_status "Setting up test environment variables..."
    
    # Export test-specific environment variables
    export TESTING=true
    export DEBUG=true
    export AUTO_VERIFY_USERS=true
    
    # Disable external services for testing
    export SENDGRID_API_KEY="dummy_api_key_for_testing"
    export MSG91_API_KEY="dummy_msg91_key"
    export S3_ACCESS_KEY="dummy_s3_access_key"
    export S3_SECRET_KEY="dummy_s3_secret_key"
    
    # Test-specific JWT settings
    export SECRET_KEY="test-secret-key-change-in-production"
    export ACCESS_TOKEN_EXPIRE_MINUTES=30
    export REFRESH_TOKEN_EXPIRE_DAYS=7
    
    print_success "Test environment variables configured"
}

# Create test configuration file
create_test_config() {
    print_status "Creating test configuration..."
    
    cat > .env.test << EOF
# Test Environment Configuration
# This file contains environment variables specifically for testing

# Test Database Configuration
TEST_DATABASE_URL=${TEST_DATABASE_URL}

# Test Settings
TESTING=true
DEBUG=true
AUTO_VERIFY_USERS=true

# Disable external services for testing
SENDGRID_API_KEY=dummy_api_key_for_testing
EMAIL_FROM_ADDRESS=test@woofzoo.test
EMAIL_FROM_NAME=Woofzoo Test

# Disable SMS services
MSG91_API_KEY=dummy_msg91_key
MSG91_TEMPLATE_ID=dummy_template
MSG91_SENDER_ID=WOOFZO

# Disable S3 storage
S3_BUCKET_NAME=woofzoo-test-bucket
S3_REGION=us-east-1
S3_ACCESS_KEY=dummy_s3_access_key
S3_SECRET_KEY=dummy_s3_secret_key

# Test-specific JWT settings
SECRET_KEY=test-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256

# Test-specific email settings
EMAIL_VERIFICATION_EXPIRE_HOURS=24
PASSWORD_RESET_EXPIRE_HOURS=24
FRONTEND_URL=http://localhost:3000

# Test-specific password settings
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_DIGITS=true
PASSWORD_REQUIRE_SPECIAL=true

# Test-specific pet settings
PET_PHOTO_MAX_SIZE_MB=5
PET_PHOTO_ALLOWED_TYPES=["image/jpeg", "image/png", "image/webp"]

# Test-specific family settings
FAMILY_INVITATION_EXPIRE_DAYS=10

# Test-specific OTP settings
OTP_EXPIRE_MINUTES=10
OTP_MAX_ATTEMPTS=3

# API settings
API_PREFIX=/api
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Application settings
APP_NAME=WoofZoo Test
APP_VERSION=0.1.0
DATABASE_ECHO=false
EOF

    print_success "Test configuration file created: .env.test"
}

# Run a quick test to verify setup
run_quick_test() {
    print_status "Running quick test to verify setup..."
    
    # Test database connection
    python3 -c "
import os
import sys
sys.path.append('.')
try:
    from tests.conftest import test_engine
    print('✅ Database connection test passed')
except Exception as e:
    print(f'❌ Database connection test failed: {e}')
    sys.exit(1)
"
    
    # Test pytest installation
    if python3 -m pytest --version &> /dev/null; then
        print_success "pytest installation verified"
    else
        print_error "pytest installation failed"
        exit 1
    fi
}

# Show usage instructions
show_instructions() {
    echo ""
    echo -e "${GREEN}🎉 Test environment setup complete!${NC}"
    echo ""
    echo "To run tests, use one of the following commands:"
    echo ""
    echo -e "${BLUE}Quick tests (in-memory SQLite):${NC}"
    echo "  pytest"
    echo ""
    echo -e "${BLUE}Tests with coverage:${NC}"
    echo "  pytest --cov=app --cov-report=html"
    echo ""
    echo -e "${BLUE}Specific test file:${NC}"
    echo "  pytest tests/test_integration_01_auth.py"
    echo ""
    echo -e "${BLUE}Verbose output:${NC}"
    echo "  pytest -v"
    echo ""
    echo -e "${BLUE}Debug mode (file-based SQLite):${NC}"
    echo "  export TEST_DATABASE_URL='sqlite:///./test_woofzoo.db'"
    echo "  pytest"
    echo ""
    echo -e "${BLUE}PostgreSQL testing:${NC}"
    echo "  export TEST_DATABASE_URL='postgresql://postgres@localhost:5432/woofzoo_test'"
    echo "  pytest"
    echo ""
    echo "For more information, see: tests/README.md"
    echo ""
}

# Main setup function
main() {
    echo -e "${GREEN}🐕 WoofZoo Test Environment Setup${NC}"
    echo "=================================="
    echo ""
    
    check_python
    check_pip
    install_dependencies
    setup_test_database
    setup_environment
    create_test_config
    run_quick_test
    show_instructions
}

# Run main function
main "$@"
