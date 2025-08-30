"""
Pet types service for managing pet types and breeds.

This module provides the PetTypesService class for pet types and breeds
business logic and data management.
"""

from app.data.pet_types import get_pet_types, get_breeds_for_type, validate_pet_type_and_breed


class PetTypesService:
    """
    Pet types service for managing pet types and breeds.
    
    This class handles business logic for pet types and breeds operations.
    """
    
    def get_pet_types(self) -> list[str]:
        """
        Get list of available pet types.
        
        Returns:
            List of available pet types
        """
        return get_pet_types()
    
    def get_breeds_for_type(self, pet_type: str) -> list[str]:
        """
        Get list of breeds for a specific pet type.
        
        Args:
            pet_type: Pet type to get breeds for
            
        Returns:
            List of breeds for the specified pet type
        """
        return get_breeds_for_type(pet_type)
    
    def validate_pet_type_and_breed(self, pet_type: str, breed: str) -> bool:
        """
        Validate if pet type and breed combination is valid.
        
        Args:
            pet_type: Pet type to validate
            breed: Breed to validate
            
        Returns:
            True if valid combination, False otherwise
        """
        return validate_pet_type_and_breed(pet_type, breed)
    
    def get_pet_type_info(self, pet_type: str) -> dict:
        """
        Get detailed information about a pet type.
        
        Args:
            pet_type: Pet type to get info for
            
        Returns:
            Dictionary with pet type information
        """
        breeds = get_breeds_for_type(pet_type)
        return {
            "pet_type": pet_type,
            "breeds": breeds,
            "breed_count": len(breeds)
        }
    
    def search_breeds(self, search_term: str, pet_type: str = None) -> list[str]:
        """
        Search breeds by name, optionally filtered by pet type.
        
        Args:
            search_term: Search term to match against breed names
            pet_type: Optional pet type filter
            
        Returns:
            List of matching breed names
        """
        search_term_lower = search_term.lower()
        
        if pet_type:
            # Search within specific pet type
            breeds = get_breeds_for_type(pet_type)
            return [breed for breed in breeds if search_term_lower in breed.lower()]
        else:
            # Search across all pet types
            all_breeds = []
            for pt in get_pet_types():
                breeds = get_breeds_for_type(pt)
                all_breeds.extend(breeds)
            
            return [breed for breed in all_breeds if search_term_lower in breed.lower()]
