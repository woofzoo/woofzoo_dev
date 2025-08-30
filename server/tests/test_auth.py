"""
Tests for authentication functionality.

This module contains tests for authentication-related functionality including
user registration, login, password reset, and token management.
"""

import pytest
from fastapi import status

from app.schemas.auth import UserSignup, UserLogin


class TestAuthAPI:
    """Test cases for authentication API endpoints."""
    
    def test_register_user_success(self, client, sample_user_data):
        """Test successful user registration."""
        response = client.post("/api/auth/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "message" in data
        assert "registered successfully" in data["message"]
    
    def test_register_user_duplicate_email(self, client, sample_user_data):
        """Test user registration with duplicate email."""
        # Register first user
        client.post("/api/auth/register", json=sample_user_data)
        
        # Try to register second user with same email
        response = client.post("/api/auth/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]
    
    def test_register_user_invalid_password(self, client, sample_user_data):
        """Test user registration with invalid password."""
        sample_user_data["password"] = "weak"
        response = client.post("/api/auth/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_user_invalid_role(self, client, sample_user_data):
        """Test user registration with invalid role."""
        sample_user_data["roles"] = ["invalid_role"]
        response = client.post("/api/auth/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_user_success(self, client, sample_user_data):
        """Test successful user login."""
        # First register a user
        client.post("/api/auth/register", json=sample_user_data)
        
        # Then login
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "user" in data
        assert "tokens" in data
        assert "access_token" in data["tokens"]
        assert "refresh_token" in data["tokens"]
        assert data["user"]["email"] == sample_user_data["email"]
    
    def test_login_user_invalid_credentials(self, client):
        """Test user login with invalid credentials."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid email or password" in response.json()["detail"]
    
    def test_request_password_reset(self, client):
        """Test password reset request."""
        reset_data = {"email": "test@example.com"}
        response = client.post("/api/auth/request-password-reset", json=reset_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "password reset" in data["message"].lower()
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication."""
        response = client.get("/api/auth/me")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_current_user_authorized(self, client, sample_user_data):
        """Test getting current user with authentication."""
        # Register and login user
        client.post("/api/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["tokens"]["access_token"]
        
        # Get current user with token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == sample_user_data["email"]
    
    def test_update_personalization(self, client, sample_user_data):
        """Test updating user personalization settings."""
        # Register and login user
        client.post("/api/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["tokens"]["access_token"]
        
        # Update personalization
        personalization_data = {"personalization": {"theme": "dark", "language": "es"}}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put("/api/auth/me/personalization", json=personalization_data, headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["personalization"]["theme"] == "dark"
        assert data["personalization"]["language"] == "es"
    
    def test_refresh_tokens(self, client, sample_user_data):
        """Test token refresh."""
        # Register and login user
        client.post("/api/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        refresh_token = login_response.json()["tokens"]["refresh_token"]
        
        # Refresh tokens
        response = client.post(f"/api/auth/refresh?refresh_token={refresh_token}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/auth/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "running" in data["message"].lower()
