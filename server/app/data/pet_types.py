"""
Pet types and breeds data for validation.

This module contains predefined lists of pet types and breeds
for validation in pet profile creation and updates.
"""

PET_TYPES_AND_BREEDS = {
    "DOG": [
        "Golden Retriever", "Labrador Retriever", "German Shepherd", "Bulldog",
        "Beagle", "Poodle", "Rottweiler", "Yorkshire Terrier", "Boxer", "Dachshund",
        "Chihuahua", "Great Dane", "Siberian Husky", "Border Collie", "Australian Shepherd",
        "Pomeranian", "Shih Tzu", "Cavalier King Charles Spaniel", "Bernese Mountain Dog",
        "Mixed Breed", "Other"
    ],
    "CAT": [
        "Persian", "Maine Coon", "Siamese", "Ragdoll", "British Shorthair",
        "Abyssinian", "Russian Blue", "Bengal", "Sphynx", "American Shorthair",
        "Exotic Shorthair", "Norwegian Forest Cat", "Scottish Fold", "Birman",
        "Oriental Shorthair", "Mixed Breed", "Other"
    ],
    "BIRD": [
        "Parrot", "Cockatiel", "Budgerigar", "Canary", "Finch",
        "Cockatoo", "Macaw", "African Grey", "Lovebird", "Conure",
        "Other"
    ],
    "FISH": [
        "Goldfish", "Betta", "Guppy", "Tetra", "Angelfish",
        "Cichlid", "Platy", "Molly", "Swordtail", "Other"
    ],
    "RABBIT": [
        "Holland Lop", "Netherland Dwarf", "Rex", "Angora", "Lionhead",
        "Flemish Giant", "Mini Rex", "Other"
    ],
    "HAMSTER": [
        "Syrian", "Dwarf Campbell", "Dwarf Winter White", "Roborovski", "Chinese",
        "Other"
    ],
    "GUINEA_PIG": [
        "American", "Abyssinian", "Peruvian", "Silkie", "Teddy",
        "Other"
    ],
    "OTHER": [
        "Ferret", "Chinchilla", "Hedgehog", "Sugar Glider", "Reptile",
        "Other"
    ]
}


def get_pet_types() -> list[str]:
    """
    Get list of available pet types.
    
    Returns:
        List of available pet types
    """
    return list(PET_TYPES_AND_BREEDS.keys())


def get_breeds_for_type(pet_type: str) -> list[str]:
    """
    Get list of breeds for a specific pet type.
    
    Args:
        pet_type: Pet type to get breeds for
        
    Returns:
        List of breeds for the specified pet type
    """
    return PET_TYPES_AND_BREEDS.get(pet_type.upper(), [])


def validate_pet_type_and_breed(pet_type: str, breed: str) -> bool:
    """
    Validate if pet type and breed combination is valid.
    
    Args:
        pet_type: Pet type to validate
        breed: Breed to validate
        
    Returns:
        True if valid combination, False otherwise
    """
    breeds = get_breeds_for_type(pet_type)
    return breed in breeds


def get_all_breeds() -> list[str]:
    """
    Get list of all available breeds across all pet types.
    
    Returns:
        List of all available breeds
    """
    all_breeds = []
    for breeds in PET_TYPES_AND_BREEDS.values():
        all_breeds.extend(breeds)
    return all_breeds
