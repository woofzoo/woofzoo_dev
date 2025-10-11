"""
OTP repository for database operations.

This module provides the OTPRepository class for managing OTP records
in the database.
"""

from typing import Optional
from datetime import datetime, timezone
import uuid

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.models.otp import OTP, OTPPurpose
from app.repositories.base import BaseRepository


class OTPRepository(BaseRepository[OTP]):
    """
    OTP repository for managing OTP records.
    
    This class extends BaseRepository to provide OTP-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the OTP repository."""
        super().__init__(OTP, session)
    
    def create(
        self,
        user_id: uuid.UUID,
        otp_code: str,
        purpose: OTPPurpose,
        expires_at: datetime,
        metadata: Optional[dict] = None
    ) -> OTP:
        """
        Create a new OTP record.
        
        Note: The OTP model uses phone_number, but we'll store user_id as string in phone_number field
        for pet access OTPs until the model is updated.
        
        Args:
            user_id: User UUID
            otp_code: 6-digit OTP code
            purpose: Purpose of the OTP
            expires_at: Expiration datetime
            metadata: Additional metadata (not stored in current model)
            
        Returns:
            Created OTP instance
        """
        otp = OTP(
            phone_number=str(user_id),  # Temporary: storing user_id as phone_number
            otp_code=otp_code,
            purpose=purpose,
            expires_at=expires_at,
            is_used=False
        )
        self.session.add(otp)
        self.session.commit()
        self.session.refresh(otp)
        return otp
    
    def get_by_code_and_user(self, otp_code: str, user_id: uuid.UUID) -> Optional[OTP]:
        """
        Get OTP by code and user ID.
        
        Args:
            otp_code: OTP code to find
            user_id: User UUID
            
        Returns:
            OTP instance if found, None otherwise
        """
        result = self.session.execute(
            select(OTP).where(
                and_(
                    OTP.otp_code == otp_code,
                    OTP.phone_number == str(user_id),  # Temporary: stored as phone_number
                    OTP.is_used == False
                )
            )
        )
        return result.scalar_one_or_none()
    
    def mark_used(self, otp_id: uuid.UUID) -> bool:
        """
        Mark an OTP as used.
        
        Args:
            otp_id: OTP record ID
            
        Returns:
            True if marked, False if not found
        """
        otp = self.get(otp_id)
        if otp:
            otp.is_used = True
            self.session.commit()
            return True
        return False
    
    def get_valid_otp(
        self,
        otp_code: str,
        user_id: uuid.UUID,
        purpose: OTPPurpose
    ) -> Optional[OTP]:
        """
        Get a valid (not used, not expired) OTP.
        
        Args:
            otp_code: OTP code
            user_id: User UUID
            purpose: Expected purpose
            
        Returns:
            Valid OTP instance or None
        """
        now = datetime.now(timezone.utc)
        result = self.session.execute(
            select(OTP).where(
                and_(
                    OTP.otp_code == otp_code,
                    OTP.phone_number == str(user_id),
                    OTP.purpose == purpose,
                    OTP.is_used == False,
                    OTP.expires_at > now
                )
            )
        )
        return result.scalar_one_or_none()

