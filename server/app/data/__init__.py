"""
Data package for the application.

This package contains data structures, constants, and validation functions
used throughout the application.
"""

from app.data.pet_types import (
    PET_TYPES_AND_BREEDS,
    get_pet_types,
    get_breeds_for_type,
    validate_pet_type_and_breed,
    get_all_breeds,
)

__all__ = [
    "PET_TYPES_AND_BREEDS",
    "get_pet_types",
    "get_breeds_for_type", 
    "validate_pet_type_and_breed",
    "get_all_breeds",
]
