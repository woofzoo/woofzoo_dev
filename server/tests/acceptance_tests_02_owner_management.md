# Phase 2: Pet Owner Management - Acceptance Tests

## Overview
This document outlines acceptance tests for the pet owner management functionality of the WoofZoo Pet Management System.

---

## Test Case 2.1: Create Owner Profile
**Given** an authenticated user wants to create an owner profile  
**When** they provide valid owner information (name, phone, email, address)  
**Then** an owner profile should be created successfully  
**And** the owner should be associated with the authenticated user  
**And** a unique owner ID should be generated  

## Test Case 2.2: Update Owner Information
**Given** an owner profile exists  
**When** the owner updates their information  
**Then** the profile should be updated successfully  
**And** the changes should be reflected immediately  
**And** the updated_at timestamp should be updated  

## Test Case 2.3: Search Owner by Phone Number
**Given** an owner profile exists with a specific phone number  
**When** a user searches for an owner using that phone number  
**Then** the owner profile should be returned  
**And** all owner information should be included in the response  

## Test Case 2.4: Search Owner by Name
**Given** multiple owner profiles exist  
**When** a user searches for owners by name  
**Then** matching owner profiles should be returned  
**And** the results should be paginated appropriately  

## Test Case 2.5: Delete Owner Profile
**Given** an owner profile exists  
**When** the owner deletes their profile  
**Then** the profile should be removed from the system  
**And** associated pets should be handled according to business rules  

## Test Case 2.6: Get Owner by ID
**Given** an owner profile exists with a specific ID  
**When** a user requests the owner information using that ID  
**Then** the complete owner profile should be returned  
**And** all associated information should be included  

## Test Case 2.7: List All Owners
**Given** multiple owner profiles exist in the system  
**When** a user requests all owners  
**Then** all owner profiles should be returned  
**And** the results should be paginated appropriately  
**And** sensitive information should be protected  

## Test Case 2.8: Owner Data Validation
**Given** a user attempts to create or update an owner profile  
**When** they provide invalid data (invalid phone format, invalid email, missing required fields)  
**Then** the operation should fail  
**And** specific validation error messages should be returned  
**And** no changes should be made to the database  

## Test Case 2.9: Owner Phone Number Uniqueness
**Given** an owner profile exists with a specific phone number  
**When** another user tries to create an owner profile with the same phone number  
**Then** the operation should fail  
**And** an appropriate error message should be returned  
**And** no duplicate owner should be created  

## Test Case 2.10: Owner Association with User
**Given** an authenticated user creates an owner profile  
**When** the owner profile is created  
**Then** the owner should be properly associated with the user  
**And** the user should have appropriate permissions to manage the owner profile  

---

## Test Execution Notes
- Owner phone numbers should be validated for proper format
- Email addresses should be validated for proper format
- Address information should be properly sanitized
- Owner-user associations should be tested for security
- Pagination should be tested with various page sizes
