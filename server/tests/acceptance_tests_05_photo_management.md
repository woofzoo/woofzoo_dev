# Phase 5: Photo Management - Acceptance Tests

## Overview
This document outlines acceptance tests for the photo management functionality of the WoofZoo Pet Management System.

---

## Test Case 5.1: Create Photo Upload Request
**Given** a pet exists in the system  
**When** a user requests to upload a photo for that pet  
**Then** a photo upload request should be created  
**And** a pre-signed upload URL should be generated  
**And** the URL should be valid for the specified duration  

## Test Case 5.2: Upload Photo Metadata
**Given** a photo has been uploaded to storage  
**When** the user submits the photo metadata  
**Then** a photo record should be created in the database  
**And** the photo should be associated with the pet  
**And** all metadata should be stored correctly  

## Test Case 5.3: Set Primary Photo
**Given** multiple photos exist for a pet  
**When** a user sets one photo as the primary photo  
**Then** that photo should be marked as primary  
**And** any previously primary photo should be marked as non-primary  

## Test Case 5.4: Get Photos by Pet
**Given** a pet has multiple photos  
**When** a user requests photos for that pet  
**Then** all photos for that pet should be returned  
**And** the results should be paginated appropriately  
**And** photo metadata should be included  

## Test Case 5.5: Get Primary Photo
**Given** a pet has a primary photo set  
**When** a user requests the primary photo for that pet  
**Then** the primary photo information should be returned  
**And** the photo should be marked as primary  

## Test Case 5.6: Generate Download URL
**Given** a photo exists in the system  
**When** a user requests a download URL for the photo  
**Then** a pre-signed download URL should be generated  
**And** the URL should be valid for the specified duration  
**And** the URL should allow secure access to the photo  

## Test Case 5.7: Update Photo Information
**Given** a photo exists in the system  
**When** a user updates the photo metadata  
**Then** the photo information should be updated successfully  
**And** the changes should be reflected immediately  

## Test Case 5.8: Soft Delete Photo
**Given** a photo exists in the system  
**When** a user deletes the photo  
**Then** the photo should be marked as deleted (soft delete)  
**And** the photo should no longer appear in regular queries  
**And** the actual file should remain in storage  

## Test Case 5.9: Hard Delete Photo
**Given** a soft-deleted photo exists  
**When** a user permanently deletes the photo  
**Then** the photo record should be removed from the database  
**And** the actual file should be deleted from storage  

## Test Case 5.10: Photo Validation
**Given** a user attempts to upload a photo  
**When** the photo doesn't meet validation requirements (wrong format, too large, etc.)  
**Then** the upload should be rejected  
**And** appropriate error messages should be returned  

## Test Case 5.11: Get Photos by Uploader
**Given** a user has uploaded multiple photos  
**When** a user requests photos uploaded by a specific user  
**Then** all photos uploaded by that user should be returned  
**And** the results should be paginated appropriately  

## Test Case 5.12: Photo File Size Limits
**Given** a user attempts to upload a photo  
**When** the photo exceeds the maximum file size limit  
**Then** the upload should be rejected  
**And** an appropriate error message should be returned  

## Test Case 5.13: Photo Format Validation
**Given** a user attempts to upload a photo  
**When** the photo is in an unsupported format  
**Then** the upload should be rejected  
**And** an appropriate error message should be returned  

## Test Case 5.14: Photo Dimension Validation
**Given** a user attempts to upload a photo  
**When** the photo dimensions are outside acceptable limits  
**Then** the upload should be rejected or processed accordingly  
**And** appropriate handling should occur  

## Test Case 5.15: Photo Storage Cleanup
**Given** photos are deleted from the system  
**When** the deletion process completes  
**Then** storage space should be properly cleaned up  
**And** orphaned files should be removed  

---

## Test Execution Notes
- Photo upload URLs should be tested for proper expiration
- File format validation should include common image formats
- File size limits should be tested with various file sizes
- Storage cleanup should be tested for proper resource management
- Photo metadata should be validated for accuracy and completeness
