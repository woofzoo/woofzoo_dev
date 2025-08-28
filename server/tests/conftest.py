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


@pytest.fixture
def sample_family_data():
    """Sample family data for testing."""
    return {
        "name": "Test Family",
        "description": "A test family for testing purposes"
    }


@pytest.fixture
def sample_family(db_session, sample_owner, sample_family_data):
    """Create a sample family in the database."""
    from app.services.family import FamilyService
    from app.repositories.family import FamilyRepository
    from app.schemas.family import FamilyCreate
    
    family_repository = FamilyRepository(db_session)
    family_service = FamilyService(family_repository)
    
    family_create = FamilyCreate(**sample_family_data)
    family = family_service.create_family(family_create, str(sample_owner.id))
    
    return family


@pytest.fixture
def sample_family_member_data():
    """Sample family member data for testing."""
    return {
        "user_id": "123e4567-e89b-12d3-a456-426614174001",
        "access_level": "MEMBER"
    }


@pytest.fixture
def sample_family_member(db_session, sample_family, sample_user, sample_family_member_data):
    """Create a sample family member in the database."""
    from app.services.family_member import FamilyMemberService
    from app.repositories.family_member import FamilyMemberRepository
    from app.schemas.family import FamilyMemberCreate
    
    family_member_repository = FamilyMemberRepository(db_session)
    family_member_service = FamilyMemberService(family_member_repository)
    
    member_data = {**sample_family_member_data, "user_id": str(sample_user.id)}
    member_create = FamilyMemberCreate(**member_data)
    member = family_member_service.add_family_member(str(sample_family.id), member_create)
    
    return member


@pytest.fixture
def sample_family_invitation_data():
    """Sample family invitation data for testing."""
    return {
        "email": "invitee@example.com",
        "access_level": "MEMBER",
        "message": "Join our family!"
    }


@pytest.fixture
def sample_family_invitation(db_session, sample_family, sample_user, sample_family_invitation_data):
    """Create a sample family invitation in the database."""
    from app.services.family_invitation import FamilyInvitationService
    from app.repositories.family_invitation import FamilyInvitationRepository
    from app.schemas.family import FamilyInvitationCreate
    
    family_invitation_repository = FamilyInvitationRepository(db_session)
    family_invitation_service = FamilyInvitationService(family_invitation_repository)
    
    invitation_create = FamilyInvitationCreate(**sample_family_invitation_data)
    invitation = family_invitation_service.create_invitation(
        str(sample_family.id), 
        invitation_create, 
        str(sample_user.id)
    )
    
    return invitation


@pytest.fixture
def sample_photo_data():
    """Sample photo data for testing."""
    return {
        "filename": "test_photo.jpg",
        "file_size": 1024000,
        "mime_type": "image/jpeg",
        "width": 1920,
        "height": 1080,
        "is_primary": False
    }


@pytest.fixture
def sample_photo_upload_data():
    """Sample photo upload data for testing."""
    return {
        "filename": "test_upload.jpg",
        "file_size": 512000,
        "mime_type": "image/jpeg",
        "is_primary": False
    }


@pytest.fixture
def sample_photo(db_session, sample_pet, sample_user, sample_photo_data):
    """Create a sample photo in the database."""
    from app.services.photo import PhotoService
    from app.repositories.photo import PhotoRepository
    from app.services.storage import StorageService
    from app.schemas.photo import PhotoCreate
    
    photo_repository = PhotoRepository(db_session)
    storage_service = StorageService()
    photo_service = PhotoService(photo_repository, storage_service)
    
    photo_data = {**sample_photo_data, "pet_id": str(sample_pet.id), "uploaded_by": sample_user.id}
    photo_create = PhotoCreate(**photo_data)
    photo = photo_service.create_photo(photo_create)
    
    return photo


@pytest.fixture
def sample_primary_photo(db_session, sample_pet, sample_user, sample_photo_data):
    """Create a sample primary photo in the database."""
    from app.services.photo import PhotoService
    from app.repositories.photo import PhotoRepository
    from app.services.storage import StorageService
    from app.schemas.photo import PhotoCreate
    
    photo_repository = PhotoRepository(db_session)
    storage_service = StorageService()
    photo_service = PhotoService(photo_repository, storage_service)
    
    photo_data = {**sample_photo_data, "pet_id": str(sample_pet.id), "uploaded_by": sample_user.id, "is_primary": True}
    photo_create = PhotoCreate(**photo_data)
    photo = photo_service.create_photo(photo_create)
    
    return photo



