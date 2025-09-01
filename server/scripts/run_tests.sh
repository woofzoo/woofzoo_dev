#!/bin/bash

# Test Runner Script
# This script provides convenient ways to run tests with different configurations

set -e

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

# Function to show usage
show_usage() {
    echo "🐕 WoofZoo Test Runner"
    echo "====================="
    echo ""
    echo "Usage: $0 [OPTIONS] [TEST_PATH]"
    echo ""
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -v, --verbose           Run with verbose output"
    echo "  -c, --coverage          Run with coverage report"
    echo "  -f, --fast              Run only fast tests (exclude slow/integration)"
    echo "  -i, --integration       Run only integration tests"
    echo "  -u, --unit              Run only unit tests"
    echo "  -d, --debug             Use file-based SQLite for debugging"
    echo "  -p, --postgres          Use PostgreSQL for testing"
    echo "  -x, --stop-on-fail      Stop on first failure"
    echo "  -k, --keep-db           Keep test database (for debugging)"
    echo "  -l, --list              List available tests"
    echo ""
    echo "Test Paths:"
    echo "  tests/                  Run all tests"
    echo "  tests/test_*.py         Run specific test file"
    echo "  tests/unit/             Run unit tests only"
    echo "  tests/integration/      Run integration tests only"
    echo ""
    echo "Examples:"
    echo "  $0                      # Run all tests with default settings"
    echo "  $0 -v                   # Run all tests with verbose output"
    echo "  $0 -c                   # Run tests with coverage report"
    echo "  $0 -f                   # Run only fast tests"
    echo "  $0 -i                   # Run only integration tests"
    echo "  $0 -d                   # Use file-based SQLite for debugging"
    echo "  $0 tests/test_integration_01_auth.py  # Run specific test file"
    echo "  $0 -v -c tests/         # Run all tests with verbose output and coverage"
    echo ""
}

# Function to setup environment
setup_environment() {
    # Load test environment if .env.test exists
    if [ -f ".env.test" ]; then
        print_status "Loading test environment from .env.test"
        # Source the file instead of exporting to avoid parsing issues
        set -a
        source .env.test
        set +a
    fi
    
    # Set default test database if not set
    if [ -z "$TEST_DATABASE_URL" ]; then
        export TEST_DATABASE_URL="sqlite:///:memory:"
    fi
    
    # Set test-specific environment variables
    export TESTING=true
    export DEBUG=true
    export AUTO_VERIFY_USERS=true
}

# Function to cleanup test database
cleanup_database() {
    if [ "$KEEP_DB" = "true" ]; then
        print_warning "Keeping test database for debugging"
        return
    fi
    
    if [[ "$TEST_DATABASE_URL" == *"test_woofzoo.db"* ]]; then
        print_status "Cleaning up test database file"
        rm -f test_woofzoo.db
    fi
}

# Function to run tests
run_tests() {
    local pytest_args=()
    
    # Add basic pytest arguments
    pytest_args+=("$@")
    
    # Add verbose flag
    if [ "$VERBOSE" = "true" ]; then
        pytest_args+=("-v")
    fi
    
    # Add coverage flag
    if [ "$COVERAGE" = "true" ]; then
        pytest_args+=("--cov=app" "--cov-report=html" "--cov-report=term")
    fi
    
    # Add stop on failure flag
    if [ "$STOP_ON_FAIL" = "true" ]; then
        pytest_args+=("-x")
    fi
    
    # Add markers for test types
    if [ "$FAST_ONLY" = "true" ]; then
        pytest_args+=("-m" "not slow")
    fi
    
    if [ "$INTEGRATION_ONLY" = "true" ]; then
        pytest_args+=("-m" "integration")
    fi
    
    if [ "$UNIT_ONLY" = "true" ]; then
        pytest_args+=("-m" "not integration")
    fi
    
    # Show what we're running
    print_status "Running tests with command: pytest ${pytest_args[*]}"
    echo ""
    
    # Run the tests
    if python -m pytest "${pytest_args[@]}"; then
        print_success "All tests passed! 🎉"
        return 0
    else
        print_error "Some tests failed! ❌"
        return 1
    fi
}

# Function to list available tests
list_tests() {
    print_status "Available tests:"
    echo ""
    
    # List test files
    if [ -d "tests" ]; then
        echo "Test files:"
        find tests -name "test_*.py" -type f | sort
        echo ""
        
        # List test functions
        echo "Test functions:"
        python -m pytest --collect-only -q 2>/dev/null | grep "::" | sort
    else
        print_warning "No tests directory found"
    fi
}

# Parse command line arguments
VERBOSE=false
COVERAGE=false
FAST_ONLY=false
INTEGRATION_ONLY=false
UNIT_ONLY=false
DEBUG_MODE=false
POSTGRES_MODE=false
STOP_ON_FAIL=false
KEEP_DB=false
LIST_TESTS=false
TEST_PATH="tests/"

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -f|--fast)
            FAST_ONLY=true
            shift
            ;;
        -i|--integration)
            INTEGRATION_ONLY=true
            shift
            ;;
        -u|--unit)
            UNIT_ONLY=true
            shift
            ;;
        -d|--debug)
            DEBUG_MODE=true
            export TEST_DATABASE_URL="sqlite:///./test_woofzoo.db"
            shift
            ;;
        -p|--postgres)
            POSTGRES_MODE=true
            export TEST_DATABASE_URL="postgresql://postgres@localhost:5432/woofzoo_test"
            shift
            ;;
        -x|--stop-on-fail)
            STOP_ON_FAIL=true
            shift
            ;;
        -k|--keep-db)
            KEEP_DB=true
            shift
            ;;
        -l|--list)
            LIST_TESTS=true
            shift
            ;;
        -*)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
        *)
            TEST_PATH="$1"
            shift
            ;;
    esac
done

# Main execution
main() {
    echo -e "${GREEN}🐕 WoofZoo Test Runner${NC}"
    echo "====================="
    echo ""
    
    # Show current configuration
    print_status "Test Database: $TEST_DATABASE_URL"
    print_status "Test Path: $TEST_PATH"
    
    if [ "$VERBOSE" = "true" ]; then
        print_status "Verbose mode: enabled"
    fi
    
    if [ "$COVERAGE" = "true" ]; then
        print_status "Coverage reporting: enabled"
    fi
    
    if [ "$FAST_ONLY" = "true" ]; then
        print_status "Fast tests only: enabled"
    fi
    
    if [ "$INTEGRATION_ONLY" = "true" ]; then
        print_status "Integration tests only: enabled"
    fi
    
    if [ "$UNIT_ONLY" = "true" ]; then
        print_status "Unit tests only: enabled"
    fi
    
    if [ "$DEBUG_MODE" = "true" ]; then
        print_status "Debug mode: enabled (file-based SQLite)"
    fi
    
    if [ "$POSTGRES_MODE" = "true" ]; then
        print_status "PostgreSQL mode: enabled"
    fi
    
    echo ""
    
    # Setup environment
    setup_environment
    
    # List tests if requested
    if [ "$LIST_TESTS" = "true" ]; then
        list_tests
        exit 0
    fi
    
    # Check if test path exists
    if [ ! -e "$TEST_PATH" ]; then
        print_error "Test path does not exist: $TEST_PATH"
        exit 1
    fi
    
    # Run tests
    if run_tests "$TEST_PATH"; then
        cleanup_database
        exit 0
    else
        cleanup_database
        exit 1
    fi
}

# Run main function
main "$@"
