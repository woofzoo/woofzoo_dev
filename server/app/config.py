"""
Configuration management for the application.

This module handles all configuration settings using Pydantic Settings
for type-safe environment variable management.
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application settings
    app_name: str = Field(default="WoofZoo", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Database settings
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/woofzoo",
        description="PostgreSQL database URL"
    )
    database_echo: bool = Field(default=False, description="Echo SQL queries")
    
    # API settings
    api_prefix: str = Field(default="/api", description="API prefix")
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS allowed origins"
    )
    
    # Security settings
    secret_key: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key for JWT tokens"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=7,
        description="Refresh token expiration time in days"
    )
    algorithm: str = Field(
        default="HS256",
        description="JWT algorithm"
    )
    
    # Email settings (Mailgun)
    mailgun_api_key: str = Field(
        default="dummy_api_key",
        description="Mailgun API key"
    )
    mailgun_domain: str = Field(
        default="sandbox25b3d4a0d8f64783982dd7f5770a0851.mailgun.org",
        description="Mailgun domain"
    )
    mailgun_from_email: str = Field(
        default="postmaster@sandbox25b3d4a0d8f64783982dd7f5770a0851.mailgun.org",
        description="Mailgun from email address"
    )
    mailgun_from_name: str = Field(
        default="WoofZoo",
        description="Mailgun from name"
    )
    
    # Email verification and password reset settings
    email_verification_expire_hours: int = Field(
        default=24,
        description="Email verification token expiration time in hours"
    )
    password_reset_expire_hours: int = Field(
        default=24,
        description="Password reset token expiration time in hours"
    )
    
    # Frontend URL for email links
    frontend_url: str = Field(
        default="http://localhost:3000",
        description="Frontend URL for email verification and password reset links"
    )
    
    # Password settings
    password_min_length: int = Field(
        default=8,
        description="Minimum password length"
    )
    password_require_uppercase: bool = Field(
        default=True,
        description="Require uppercase letters in password"
    )
    password_require_lowercase: bool = Field(
        default=True,
        description="Require lowercase letters in password"
    )
    password_require_digits: bool = Field(
        default=True,
        description="Require digits in password"
    )
    password_require_special: bool = Field(
        default=True,
        description="Require special characters in password"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
