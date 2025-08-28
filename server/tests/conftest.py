"""
Pytest configuration and fixtures for testing.

This module provides test fixtures and configuration for the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db_session, Base
from app.models import User, Owner, Family, FamilyMember, Pet, OTP, FamilyInvitation


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override dependency to use test database."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the database dependency
app.dependency_overrides[get_db_session] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    yield session
    
    # Clean up
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a test client with database session."""
    return TestClient(app)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPass123!",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890",
        "roles": ["pet_owner"]
    }


@pytest.fixture
def sample_owner_data():
    """Sample owner data for testing."""
    return {
        "phone_number": "+1234567890",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "address": "123 Main St, City, State 12345"
    }


@pytest.fixture
def sample_pet_data():
    """Sample pet data for testing."""
    return {
        "name": "Buddy",
        "pet_type": "DOG",
        "breed": "Golden Retriever",
        "age": 3,
        "gender": "MALE",
        "weight": 25.5,
        "photos": ["https://example.com/photo1.jpg"],
        "emergency_contacts": {
            "vet": {"name": "Dr. Smith", "phone": "+1234567890"},
            "owner": {"name": "John Doe", "phone": "+1234567890"}
        },
        "insurance_info": {
            "provider": "PetCare Insurance",
            "policy_number": "PC123456789"
        }
    }


@pytest.fixture
def sample_user(db_session, sample_user_data):
    """Create a sample user in the database."""
    from app.services.auth import AuthService
    from app.repositories.user import UserRepository
    from app.schemas.auth import UserSignup
    
    user_repository = UserRepository(db_session)
    auth_service = AuthService(user_repository)
    
    user_signup = UserSignup(**sample_user_data)
    user = auth_service.create_user(user_signup)
    
    return user


@pytest.fixture
def sample_owner(db_session, sample_owner_data):
    """Create a sample owner in the database."""
    from app.services.owner import OwnerService
    from app.repositories.owner import OwnerRepository
    from app.schemas.owner import OwnerCreate
    
    owner_repository = OwnerRepository(db_session)
    owner_service = OwnerService(owner_repository)
    
    owner_create = OwnerCreate(**sample_owner_data)
    owner = owner_service.create_owner(owner_create)
    
    return owner


@pytest.fixture
def sample_pet(db_session, sample_owner, sample_pet_data):
    """Create a sample pet in the database."""
    from app.services.pet import PetService
    from app.repositories.pet import PetRepository
    from app.services.pet_id import PetIDService
    from app.schemas.pet import PetCreate
    
    pet_repository = PetRepository(db_session)
    pet_id_service = PetIDService(db_session)
    pet_service = PetService(pet_repository, pet_id_service)
    
    pet_data = {**sample_pet_data, "owner_id": str(sample_owner.id)}
    pet_create = PetCreate(**pet_data)
    pet = pet_service.create_pet(pet_create)
    
    return pet



