"""
Tests for authentication functionality.

This module contains tests for authentication-related functionality including
API endpoints, service layer, and repository layer.
"""

import pytest
from fastapi import status
from httpx import AsyncClient

from app.schemas.auth import UserSignup, UserLogin


class TestAuthAPI:
    """Test cases for authentication API endpoints."""
    
    @pytest.mark.asyncio
    async def test_register_user_success(self, client: AsyncClient):
        """Test successful user registration."""
        user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "password": "SecurePass123!",
            "roles": ["pet_owner"]
        }
        
        response = await client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "message" in data
        assert "User registered successfully" in data["message"]
    
    @pytest.mark.asyncio
    async def test_register_user_duplicate_email(self, client: AsyncClient):
        """Test user registration with duplicate email."""
        user_data = {
            "email": "duplicate@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "password": "SecurePass123!",
            "roles": ["pet_owner"]
        }
        
        # Register first user
        response1 = await client.post("/api/auth/register", json=user_data)
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Try to register second user with same email
        response2 = await client.post("/api/auth/register", json=user_data)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response2.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_register_user_invalid_password(self, client: AsyncClient):
        """Test user registration with invalid password."""
        user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "password": "weak",  # Too short
            "roles": ["pet_owner"]
        }
        
        response = await client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    @pytest.mark.asyncio
    async def test_register_user_invalid_role(self, client: AsyncClient):
        """Test user registration with invalid role."""
        user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "password": "SecurePass123!",
            "roles": ["invalid_role"]
        }
        
        response = await client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    @pytest.mark.asyncio
    async def test_login_user_success(self, client: AsyncClient):
        """Test successful user login."""
        # First register a user
        user_data = {
            "email": "login@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "password": "SecurePass123!",
            "roles": ["pet_owner"]
        }
        
        await client.post("/api/auth/register", json=user_data)
        
        # Then login
        login_data = {
            "email": "login@example.com",
            "password": "SecurePass123!"
        }
        
        response = await client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "user" in data
        assert "tokens" in data
        assert data["user"]["email"] == "login@example.com"
        assert "access_token" in data["tokens"]
        assert "refresh_token" in data["tokens"]
    
    @pytest.mark.asyncio
    async def test_login_user_invalid_credentials(self, client: AsyncClient):
        """Test user login with invalid credentials."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "WrongPassword123!"
        }
        
        response = await client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid email or password" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_request_password_reset(self, client: AsyncClient):
        """Test password reset request."""
        reset_data = {
            "email": "reset@example.com"
        }
        
        response = await client.post("/api/auth/request-password-reset", json=reset_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "password reset link has been sent" in data["message"]
    
    @pytest.mark.asyncio
    async def test_get_current_user_unauthorized(self, client: AsyncClient):
        """Test getting current user without authentication."""
        response = await client.get("/api/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @pytest.mark.asyncio
    async def test_get_current_user_authorized(self, client: AsyncClient):
        """Test getting current user with authentication."""
        # First register and login a user
        user_data = {
            "email": "me@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "password": "SecurePass123!",
            "roles": ["pet_owner"]
        }
        
        await client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "email": "me@example.com",
            "password": "SecurePass123!"
        }
        
        login_response = await client.post("/api/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]
        
        # Get current user with token
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        response = await client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "me@example.com"
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
    
    @pytest.mark.asyncio
    async def test_update_personalization(self, client: AsyncClient):
        """Test updating user personalization settings."""
        # First register and login a user
        user_data = {
            "email": "personalize@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "password": "SecurePass123!",
            "roles": ["pet_owner"]
        }
        
        await client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "email": "personalize@example.com",
            "password": "SecurePass123!"
        }
        
        login_response = await client.post("/api/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]
        
        # Update personalization
        personalization_data = {
            "personalization": {
                "theme": "dark",
                "language": "en",
                "notifications": {
                    "email": True,
                    "push": False
                }
            }
        }
        
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        response = await client.put("/api/auth/me/personalization", json=personalization_data, headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["personalization"]["theme"] == "dark"
        assert data["personalization"]["language"] == "en"
        assert data["personalization"]["notifications"]["email"] is True
        assert data["personalization"]["notifications"]["push"] is False
    
    @pytest.mark.asyncio
    async def test_refresh_tokens(self, client: AsyncClient):
        """Test token refresh functionality."""
        # First register and login a user
        user_data = {
            "email": "refresh@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "password": "SecurePass123!",
            "roles": ["pet_owner"]
        }
        
        await client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "email": "refresh@example.com",
            "password": "SecurePass123!"
        }
        
        login_response = await client.post("/api/auth/login", json=login_data)
        tokens = login_response.json()["tokens"]
        
        # Refresh tokens
        response = await client.post(f"/api/auth/refresh?refresh_token={tokens['refresh_token']}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Test authentication service health check."""
        response = await client.get("/api/auth/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "running" in data["message"]
