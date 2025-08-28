"""
Pet ID generation service.

This module provides services for generating unique pet IDs
in the format {TYPE}-{BREED}-{6-digit-number}.
"""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.pet import Pet
from app.data.pet_types import validate_pet_type_and_breed


class PetIDService:
    """
    Service for generating unique pet IDs.
    
    This service handles the generation of unique pet IDs in the format:
    {TYPE}-{BREED}-{6-digit-number}
    Example: DOG-GOLDEN_RETRIEVER-000001
    """
    
    def __init__(self, session: Session):
        """
        Initialize the Pet ID service.
        
        Args:
            session: Database session
        """
        self.session = session
    
    def generate_pet_id(self, pet_type: str, breed: str) -> str:
        """
        Generate unique pet ID in format: {TYPE}-{BREED}-{6-digit-number}
        
        Args:
            pet_type: Type of pet (DOG, CAT, BIRD, etc.)
            breed: Breed of the pet
            
        Returns:
            Unique pet ID string
            
        Raises:
            ValueError: If pet type or breed is invalid
        """
        # Validate pet type and breed
        if not validate_pet_type_and_breed(pet_type, breed):
            raise ValueError(f"Invalid pet type '{pet_type}' or breed '{breed}'")
        
        # Normalize breed name for ID
        normalized_breed = self._normalize_breed_name(breed)
        
        # Get next sequence number for this type-breed combination
        sequence = self._get_next_sequence(pet_type, normalized_breed)
        
        # Format: {TYPE}-{BREED}-{6-digit-number}
        return f"{pet_type.upper()}-{normalized_breed.upper()}-{sequence:06d}"
    
    def _normalize_breed_name(self, breed: str) -> str:
        """
        Normalize breed name for ID generation.
        
        Args:
            breed: Original breed name
            
        Returns:
            Normalized breed name
        """
        # Replace spaces and special characters with underscores
        normalized = breed.replace(" ", "_").replace("-", "_")
        # Remove any other special characters
        normalized = "".join(c for c in normalized if c.isalnum() or c == "_")
        return normalized
    
    def _get_next_sequence(self, pet_type: str, breed: str) -> int:
        """
        Get next sequence number for pet type-breed combination.
        
        Args:
            pet_type: Type of pet
            breed: Breed of pet
            
        Returns:
            Next sequence number
        """
        # Query existing pets with same type-breed prefix
        prefix = f"{pet_type.upper()}-{breed.upper()}-"
        
        result = self.session.execute(
            select(Pet.pet_id)
            .where(Pet.pet_id.like(f"{prefix}%"))
            .order_by(Pet.pet_id.desc())
            .limit(1)
        )
        
        last_pet_id = result.scalar_one_or_none()
        
        if last_pet_id:
            # Extract sequence number from last pet ID
            sequence_str = last_pet_id.split("-")[-1]
            return int(sequence_str) + 1
        else:
            # First pet of this type-breed combination
            return 1
    
    def validate_pet_id_format(self, pet_id: str) -> bool:
        """
        Validate if a pet ID follows the correct format.
        
        Args:
            pet_id: Pet ID to validate
            
        Returns:
            True if format is valid, False otherwise
        """
        try:
            parts = pet_id.split("-")
            if len(parts) != 3:
                return False
            
            pet_type, breed, sequence = parts
            
            # Check if sequence is a 6-digit number
            if not sequence.isdigit() or len(sequence) != 6:
                return False
            
            # Check if pet type and breed are valid
            return validate_pet_type_and_breed(pet_type, breed)
            
        except Exception:
            return False
    
    def extract_pet_info_from_id(self, pet_id: str) -> Optional[dict]:
        """
        Extract pet type and breed from a pet ID.
        
        Args:
            pet_id: Pet ID to extract info from
            
        Returns:
            Dictionary with pet_type and breed, or None if invalid
        """
        if not self.validate_pet_id_format(pet_id):
            return None
        
        parts = pet_id.split("-")
        pet_type, breed, sequence = parts
        
        # Convert normalized breed back to original format
        original_breed = breed.replace("_", " ")
        
        return {
            "pet_type": pet_type,
            "breed": original_breed,
            "sequence": int(sequence)
        }
