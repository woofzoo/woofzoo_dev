"""
Configuration management for the application.

This module handles all configuration settings using Pydantic Settings
for type-safe environment variable management.
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Pydantic settings configuration (v2)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore unknown env vars (e.g., legacy MAILGUN_*)
    )
    
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
    
    # Email settings (SendGrid)
    sendgrid_api_key: str = Field(
        default="",
        description="SendGrid API key"
    )
    email_from_address: str = Field(
        default="noreply@woofzoo.com",
        description="Default from email address"
    )
    email_from_name: str = Field(
        default="WoofZoo",
        description="Default from name"
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
    
    # Development settings
    auto_verify_users: bool = Field(
        default=False,
        description="Auto-verify users in development mode (skips email verification)"
    )
    
    # Pet Profile Settings
    pet_photo_max_size_mb: int = Field(
        default=5, 
        description="Maximum pet photo size in MB"
    )
    pet_photo_allowed_types: list[str] = Field(
        default=["image/jpeg", "image/png", "image/webp"], 
        description="Allowed image MIME types"
    )
    
    # Family Management Settings
    family_invitation_expire_days: int = Field(
        default=10, 
        description="Family invitation expiry in days"
    )
    
    # OTP Settings
    otp_expire_minutes: int = Field(
        default=10, 
        description="OTP expiry time in minutes"
    )
    otp_max_attempts: int = Field(
        default=3, 
        description="Maximum OTP attempts"
    )
    
    # MSG91 SMS Settings
    msg91_api_key: str = Field(
        default="", 
        description="MSG91 API key"
    )
    msg91_template_id: str = Field(
        default="", 
        description="MSG91 template ID"
    )
    msg91_sender_id: str = Field(
        default="WOOFZO", 
        description="MSG91 sender ID"
    )
    
    # S3 Settings
    s3_bucket_name: str = Field(
        default="woofzoo-pet-photos", 
        description="S3 bucket for pet photos"
    )
    s3_region: str = Field(
        default="us-east-1", 
        description="S3 region"
    )
    s3_access_key: str = Field(
        default="", 
        description="S3 access key"
    )
    s3_secret_key: str = Field(
        default="", 
        description="S3 secret key"
    )
    
    # Note: legacy Config class removed in favor of model_config above


# Global settings instance
settings = Settings()
