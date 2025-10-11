"""
Clinic Workflow schemas for request/response validation.

This module defines Pydantic models for clinic workflow operations including
pet search, OTP verification, pre-checks, and doctor assignment.
"""

from typing import Optional, Literal
from datetime import datetime
import uuid

from pydantic import BaseModel, Field, ConfigDict, EmailStr


# ============================================================================
# Pet Search Schemas
# ============================================================================

class PetSearchRequest(BaseModel):
    """Schema for pet search request."""
    
    search_type: Literal["email", "phone", "pet_id"] = Field(
        ..., 
        description="Type of search to perform"
    )
    search_value: str = Field(
        ..., 
        min_length=1,
        description="Value to search for"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "search_type": "email",
                "search_value": "owner@example.com"
            }
        }
    )


class OwnerBasicInfo(BaseModel):
    """Basic owner information for search results."""
    
    id: str = Field(..., description="Owner user ID")
    name: str = Field(..., description="Owner full name")
    email: str = Field(..., description="Owner email")
    phone: Optional[str] = Field(None, description="Owner phone number")
    
    model_config = ConfigDict(from_attributes=True)


class PetBasicInfo(BaseModel):
    """Basic pet information for search results."""
    
    id: str = Field(..., description="Pet UUID")
    pet_id: str = Field(..., description="Pet readable ID (e.g., DOG-001)")
    name: str = Field(..., description="Pet name")
    pet_type: str = Field(..., description="Pet type")
    breed: str = Field(..., description="Pet breed")
    age: Optional[int] = Field(None, description="Pet age in years")
    gender: Optional[str] = Field(None, description="Pet gender")
    owner: OwnerBasicInfo = Field(..., description="Pet owner information")
    
    model_config = ConfigDict(from_attributes=True)


class PetSearchResponse(BaseModel):
    """Schema for pet search response."""
    
    found: bool = Field(..., description="Whether pet was found")
    pet: Optional[PetBasicInfo] = Field(None, description="Pet information if found")
    message: Optional[str] = Field(None, description="Message if not found")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "found": True,
                "pet": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "pet_id": "DOG-GOLDEN-RETRIEVER-000001",
                    "name": "Buddy",
                    "pet_type": "DOG",
                    "breed": "Golden Retriever",
                    "age": 3,
                    "gender": "MALE",
                    "owner": {
                        "id": "user-uuid",
                        "name": "John Doe",
                        "email": "owner@example.com",
                        "phone": "+1234567890"
                    }
                }
            }
        }
    )


# ============================================================================
# OTP Request Schemas
# ============================================================================

class OTPRequestData(BaseModel):
    """Schema for OTP request."""
    
    pet_id: str = Field(..., description="Pet UUID to request access for")
    purpose: Optional[str] = Field(
        "Clinic visit and doctor assignment",
        description="Purpose of the OTP request"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_id": "550e8400-e29b-41d4-a716-446655440000",
                "purpose": "Annual checkup visit"
            }
        }
    )


class OTPRequestResponse(BaseModel):
    """Schema for OTP request response."""
    
    otp_id: str = Field(..., description="OTP record ID")
    message: str = Field(..., description="Success message")
    owner_email: str = Field(..., description="Email where OTP was sent")
    expires_in_minutes: int = Field(..., description="OTP validity period")
    otp_code: Optional[str] = Field(None, description="OTP code (DEV ONLY)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "otp_id": "uuid",
                "message": "OTP sent to pet owner's email",
                "owner_email": "owner@example.com",
                "expires_in_minutes": 10,
                "otp_code": "123456"
            }
        }
    )


# ============================================================================
# OTP Verification Schemas
# ============================================================================

class OTPVerifyRequest(BaseModel):
    """Schema for OTP verification request."""
    
    pet_id: str = Field(..., description="Pet UUID")
    otp_code: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_id": "550e8400-e29b-41d4-a716-446655440000",
                "otp_code": "123456"
            }
        }
    )


class OTPVerifyResponse(BaseModel):
    """Schema for OTP verification response."""
    
    success: bool = Field(..., description="Whether OTP was verified")
    message: str = Field(..., description="Success/error message")
    access_record_id: str = Field(..., description="Created access record ID")
    queue_status: str = Field(..., description="Current queue status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "OTP verified successfully. Pet ready for pre-checks.",
                "access_record_id": "uuid",
                "queue_status": "pending_precheck"
            }
        }
    )


# ============================================================================
# Pre-Check Vitals Schemas
# ============================================================================

class PreCheckVitalsUpdate(BaseModel):
    """Schema for updating pre-check vitals."""
    
    weight: Optional[float] = Field(None, ge=0.1, le=500, description="Weight in kg")
    temperature: Optional[float] = Field(None, ge=30, le=45, description="Temperature in °C")
    heart_rate: Optional[int] = Field(None, ge=20, le=300, description="Heart rate in BPM")
    respiratory_rate: Optional[int] = Field(None, ge=5, le=100, description="Respiratory rate")
    notes: Optional[str] = Field(None, max_length=500, description="Pre-check observations")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "weight": 25.5,
                "temperature": 38.5,
                "heart_rate": 90,
                "respiratory_rate": 25,
                "notes": "Pet is alert and responsive"
            }
        }
    )


class PreCheckVitalsResponse(BaseModel):
    """Schema for pre-check vitals response."""
    
    success: bool = Field(..., description="Whether update was successful")
    message: str = Field(..., description="Success message")
    access_record_id: str = Field(..., description="Access record ID")
    queue_status: str = Field(..., description="Updated queue status")
    pre_checks: dict = Field(..., description="Recorded pre-check data")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Pre-check vitals recorded successfully",
                "access_record_id": "uuid",
                "queue_status": "ready_for_doctor",
                "pre_checks": {
                    "weight": 25.5,
                    "temperature": 38.5,
                    "heart_rate": 90,
                    "respiratory_rate": 25,
                    "notes": "Pet is alert and responsive",
                    "recorded_at": "2025-10-11T10:05:00Z",
                    "recorded_by": "clinic_staff_user_id"
                }
            }
        }
    )


# ============================================================================
# Doctor Assignment Schemas
# ============================================================================

class AssignDoctorRequest(BaseModel):
    """Schema for assigning pet to doctor."""
    
    doctor_id: str = Field(..., description="Doctor profile UUID")
    visit_type: str = Field(..., description="Type of visit")
    chief_complaint: Optional[str] = Field(None, description="Reason for visit")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "doctor_id": "uuid",
                "visit_type": "ROUTINE_CHECKUP",
                "chief_complaint": "Annual checkup"
            }
        }
    )


class AssignDoctorResponse(BaseModel):
    """Schema for doctor assignment response."""
    
    success: bool = Field(..., description="Whether assignment was successful")
    message: str = Field(..., description="Success message")
    access_record: dict = Field(..., description="Updated access record")
    medical_record: dict = Field(..., description="Created medical record")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Pet assigned to doctor successfully",
                "access_record": {
                    "id": "uuid",
                    "pet_id": "uuid",
                    "doctor_id": "uuid",
                    "queue_status": "with_doctor",
                    "queue_position": 3
                },
                "medical_record": {
                    "id": "uuid",
                    "visit_date": "2025-10-11T10:00:00Z"
                }
            }
        }
    )

