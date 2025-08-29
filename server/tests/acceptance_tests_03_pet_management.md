# Phase 3: Pet Management Core - Acceptance Tests

## Overview
This document outlines acceptance tests for the core pet management functionality of the WoofZoo Pet Management System.

---

## Test Case 3.1: Create New Pet
**Given** an authenticated user with an owner profile  
**When** they create a new pet with valid information (name, type, breed, age, etc.)  
**Then** a pet should be created successfully  
**And** a unique pet ID should be generated  
**And** the pet should be associated with the owner  
**And** all pet information should be stored correctly  

## Test Case 3.2: Pet ID Uniqueness
**Given** multiple pets exist in the system  
**When** new pets are created  
**Then** each pet should have a unique pet ID  
**And** no duplicate pet IDs should be generated  

## Test Case 3.3: Update Pet Information
**Given** a pet profile exists  
**When** the owner updates the pet's information  
**Then** the pet profile should be updated successfully  
**And** the changes should be reflected immediately  
**And** the updated_at timestamp should be updated  

## Test Case 3.4: Get Pet by ID
**Given** a pet exists with a specific ID  
**When** a user requests the pet information using that ID  
**Then** the complete pet profile should be returned  
**And** all associated information should be included  

## Test Case 3.5: Get Pets by Owner
**Given** an owner has multiple pets  
**When** a user requests all pets for that owner  
**Then** all pets belonging to that owner should be returned  
**And** the results should be paginated appropriately  

## Test Case 3.6: Search Pets by Name
**Given** multiple pets exist with different names  
**When** a user searches for pets by name  
**Then** pets with matching names should be returned  
**And** the search should be case-insensitive  
**And** partial matches should be supported  

## Test Case 3.7: Search Pets by Breed
**Given** multiple pets exist with different breeds  
**When** a user searches for pets by breed  
**Then** pets with matching breeds should be returned  
**And** the search should be case-insensitive  

## Test Case 3.8: Get Pets by Type
**Given** pets of different types exist (dogs, cats, etc.)  
**When** a user requests pets of a specific type  
**Then** only pets of that type should be returned  
**And** the results should be paginated appropriately  

## Test Case 3.9: Delete Pet
**Given** a pet profile exists  
**When** the owner deletes the pet  
**Then** the pet should be removed from the system  
**And** associated photos should be handled according to business rules  

## Test Case 3.10: Public Pet Lookup
**Given** a pet exists with a unique pet ID  
**When** anyone (including unauthenticated users) looks up the pet using the pet ID  
**Then** the pet's public information should be returned  
**And** sensitive information should be protected  

## Test Case 3.11: Pet Data Validation
**Given** a user attempts to create or update a pet  
**When** they provide invalid data (invalid age, invalid weight, missing required fields)  
**Then** the operation should fail  
**And** specific validation error messages should be returned  
**And** no changes should be made to the database  

## Test Case 3.12: Pet Emergency Contacts
**Given** a pet profile exists with emergency contact information  
**When** the pet information is retrieved  
**Then** the emergency contact information should be included  
**And** the information should be properly formatted  

## Test Case 3.13: Pet Insurance Information
**Given** a pet profile exists with insurance information  
**When** the pet information is retrieved  
**Then** the insurance information should be included  
**And** the information should be properly formatted  

## Test Case 3.14: Pet Photos Association
**Given** a pet has multiple photos  
**When** the pet information is retrieved  
**Then** the photo URLs should be included  
**And** the primary photo should be clearly identified  

## Test Case 3.15: Pet Age Calculation
**Given** a pet has a birth date recorded  
**When** the pet information is retrieved  
**Then** the calculated age should be accurate  
**And** the age should be updated automatically over time  

---

## Test Execution Notes
- Pet IDs should be tested for uniqueness across large datasets
- Pet type and breed validation should be tested against predefined lists
- Age and weight validation should include boundary conditions
- Emergency contact and insurance information should be properly validated
- Photo associations should be tested for proper linking and unlinking
