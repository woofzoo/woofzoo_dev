"""
Tests for authentication system functionality.

This module contains tests for authentication-related functionality including
API endpoints, service layer, and middleware.
"""

import pytest
from datetime import datetime, timedelta
from fastapi import status

from app.schemas.auth import UserSignup, UserLogin, PasswordResetRequest, RefreshTokenRequest


class TestAuthenticationAPI:
    """Test cases for authentication API endpoints."""
    
    def test_register_user_success(self, client, sample_user_data):
        """Test successful user registration."""
        response = client.post("/api/auth/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "message" in data
        assert "user" in data
        assert data["user"]["email"] == sample_user_data["email"]
        assert data["user"]["first_name"] == sample_user_data["first_name"]
        assert data["user"]["last_name"] == sample_user_data["last_name"]
        assert "id" in data["user"]
        assert "is_verified" in data["user"]
    
    def test_register_user_duplicate_email(self, client, sample_user_data, sample_user):
        """Test user registration with duplicate email."""
        response = client.post("/api/auth/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]
    
    def test_register_user_invalid_data(self, client):
        """Test user registration with invalid data."""
        invalid_data = {
            "email": "invalid-email",
            "password": "123",
            "first_name": "",
            "last_name": ""
        }
        response = client.post("/api/auth/register", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_user_success(self, client, sample_user_data, sample_user):
        """Test successful user login."""
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert "expires_in" in data
        assert "user" in data
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
    
    def test_login_user_invalid_data(self, client):
        """Test user login with invalid data."""
        invalid_data = {
            "email": "invalid-email",
            "password": ""
        }
        response = client.post("/api/auth/login", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_refresh_token_success(self, client, sample_user_data, sample_user):
        """Test successful token refresh."""
        # First login to get tokens
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh token
        refresh_data = {"refresh_token": refresh_token}
        response = client.post("/api/auth/refresh", json=refresh_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert "expires_in" in data
    
    def test_refresh_token_invalid(self, client):
        """Test token refresh with invalid token."""
        refresh_data = {"refresh_token": "invalid-token"}
        response = client.post("/api/auth/refresh", json=refresh_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid refresh token" in response.json()["detail"]
    
    def test_logout_user_success(self, client, sample_user_data, sample_user):
        """Test successful user logout."""
        # First login to get access token
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]
        
        # Logout
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/api/auth/logout", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert "Logged out successfully" in response.json()["message"]
    
    def test_logout_user_unauthorized(self, client):
        """Test user logout without authentication."""
        response = client.post("/api/auth/logout")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user_success(self, client, sample_user_data, sample_user):
        """Test successful current user retrieval."""
        # First login to get access token
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]
        
        # Get current user
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["first_name"] == sample_user_data["first_name"]
        assert data["last_name"] == sample_user_data["last_name"]
        assert "id" in data
        assert "roles" in data
        assert "is_active" in data
        assert "is_verified" in data
    
    def test_get_current_user_unauthorized(self, client):
        """Test current user retrieval without authentication."""
        response = client.get("/api/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_request_password_reset_success(self, client, sample_user):
        """Test successful password reset request."""
        reset_data = {"email": sample_user.email}
        response = client.post("/api/auth/password-reset-request", json=reset_data)
        
        assert response.status_code == status.HTTP_200_OK
        assert "Password reset email sent" in response.json()["message"]
    
    def test_request_password_reset_nonexistent_email(self, client):
        """Test password reset request with nonexistent email."""
        reset_data = {"email": "nonexistent@example.com"}
        response = client.post("/api/auth/password-reset-request", json=reset_data)
        
        assert response.status_code == status.HTTP_200_OK
        assert "If the email exists" in response.json()["message"]
    
    def test_request_password_reset_invalid_data(self, client):
        """Test password reset request with invalid data."""
        reset_data = {"email": "invalid-email"}
        response = client.post("/api/auth/password-reset-request", json=reset_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_change_password_success(self, client, sample_user_data, sample_user):
        """Test successful password change."""
        # First login to get access token
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]
        
        # Change password
        headers = {"Authorization": f"Bearer {access_token}"}
        change_data = {
            "current_password": sample_user_data["password"],
            "new_password": "newpassword123"
        }
        response = client.post("/api/auth/change-password", json=change_data, headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert "Password changed successfully" in response.json()["message"]
    
    def test_change_password_invalid_current_password(self, client, sample_user_data, sample_user):
        """Test password change with invalid current password."""
        # First login to get access token
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]
        
        # Change password with wrong current password
        headers = {"Authorization": f"Bearer {access_token}"}
        change_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword123"
        }
        response = client.post("/api/auth/change-password", json=change_data, headers=headers)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid current password" in response.json()["detail"]
    
    def test_change_password_unauthorized(self, client):
        """Test password change without authentication."""
        change_data = {
            "current_password": "oldpassword",
            "new_password": "newpassword123"
        }
        response = client.post("/api/auth/change-password", json=change_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_send_verification_email_success(self, client, sample_user_data, sample_user):
        """Test successful verification email sending."""
        # First login to get access token
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]
        
        # Send verification email
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/api/auth/send-verification-email", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert "Verification email sent successfully" in response.json()["message"]
    
    def test_send_verification_email_unauthorized(self, client):
        """Test verification email sending without authentication."""
        response = client.post("/api/auth/send-verification-email")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthenticationMiddleware:
    """Test cases for authentication middleware."""
    
    def test_protected_route_with_valid_token(self, client, sample_user_data, sample_user):
        """Test accessing protected route with valid token."""
        # First login to get access token
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]
        
        # Access protected route
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_protected_route_without_token(self, client):
        """Test accessing protected route without token."""
        response = client.get("/api/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_protected_route_with_invalid_token(self, client):
        """Test accessing protected route with invalid token."""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_protected_route_with_expired_token(self, client):
        """Test accessing protected route with expired token."""
        # This would require a token that's actually expired
        # For now, we'll test with an obviously invalid token
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestJWTService:
    """Test cases for JWT service functionality."""
    
    def test_create_access_token(self, jwt_service):
        """Test access token creation."""
        data = {"sub": "123", "email": "test@example.com", "roles": ["user"]}
        token = jwt_service.create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_refresh_token(self, jwt_service):
        """Test refresh token creation."""
        data = {"sub": "123", "email": "test@example.com"}
        token = jwt_service.create_refresh_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_valid_token(self, jwt_service):
        """Test verification of valid token."""
        data = {"sub": "123", "email": "test@example.com"}
        token = jwt_service.create_access_token(data)
        
        payload = jwt_service.verify_access_token(token)
        
        assert payload is not None
        assert payload["sub"] == "123"
        assert payload["email"] == "test@example.com"
    
    def test_verify_invalid_token(self, jwt_service):
        """Test verification of invalid token."""
        payload = jwt_service.verify_access_token("invalid-token")
        
        assert payload is None
    
    def test_verify_expired_token(self, jwt_service):
        """Test verification of expired token."""
        # Create a token with very short expiration
        data = {"sub": "123", "email": "test@example.com"}
        token = jwt_service.create_access_token(data, expires_delta=timedelta(seconds=1))
        
        # Wait for token to expire
        import time
        time.sleep(2)
        
        payload = jwt_service.verify_access_token(token)
        
        assert payload is None
    
    def test_create_token_pair(self, jwt_service):
        """Test creation of token pair."""
        user_id = 123
        email = "test@example.com"
        roles = ["user", "admin"]
        
        tokens = jwt_service.create_token_pair(user_id, email, roles)
        
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["access_token"] is not None
        assert tokens["refresh_token"] is not None
    
    def test_refresh_access_token(self, jwt_service):
        """Test refreshing access token."""
        # Create token pair
        user_id = 123
        email = "test@example.com"
        roles = ["user"]
        tokens = jwt_service.create_token_pair(user_id, email, roles)
        
        # Refresh access token
        new_access_token = jwt_service.refresh_access_token(tokens["refresh_token"])
        
        assert new_access_token is not None
        assert isinstance(new_access_token, str)
        assert len(new_access_token) > 0
    
    def test_refresh_invalid_token(self, jwt_service):
        """Test refreshing with invalid token."""
        new_access_token = jwt_service.refresh_access_token("invalid-token")
        
        assert new_access_token is None
