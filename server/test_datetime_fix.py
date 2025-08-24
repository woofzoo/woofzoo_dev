#!/usr/bin/env python3
"""
Test script to verify the datetime timezone fix.
"""

import asyncio
import httpx
from datetime import datetime, timezone, timedelta

async def test_datetime_fix():
    """Test the datetime timezone fix."""
    
    print("🧪 Testing datetime timezone fix...")
    
    # Test 1: Check timezone-aware datetime creation
    print("\n1️⃣ Testing timezone-aware datetime creation:")
    utc_now = datetime.now(timezone.utc)
    print(f"   UTC now: {utc_now}")
    print(f"   Timezone: {utc_now.tzinfo}")
    
    # Test 2: Test token expiration logic
    print("\n2️⃣ Testing token expiration logic:")
    # Create a token that expires in 1 hour
    expires_in_1_hour = datetime.now(timezone.utc) + timedelta(hours=1)
    print(f"   Token expires at: {expires_in_1_hour}")
    print(f"   Current time: {utc_now}")
    print(f"   Is expired? {utc_now > expires_in_1_hour}")
    
    # Create a token that expired 1 hour ago
    expired_1_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    print(f"   Token expired at: {expired_1_hour_ago}")
    print(f"   Is expired? {utc_now > expired_1_hour_ago}")
    
    # Test 3: Test API registration
    print("\n3️⃣ Testing API registration with timezone fix:")
    
    async with httpx.AsyncClient() as client:
        register_data = {
            "email": "timezone_test@example.com",
            "first_name": "Timezone",
            "last_name": "Test",
            "password": "SecurePass123!",
            "roles": ["pet_owner"]
        }
        
        response = await client.post(
            "http://localhost:8000/api/auth/register",
            json=register_data
        )
        
        print(f"   Registration status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 201:
            print("   ✅ Registration successful!")
            
            # Test login
            login_data = {
                "email": "timezone_test@example.com",
                "password": "SecurePass123!"
            }
            
            login_response = await client.post(
                "http://localhost:8000/api/auth/login",
                json=login_data
            )
            
            print(f"   Login status: {login_response.status_code}")
            if login_response.status_code == 200:
                print("   ✅ Login successful!")
                login_data = login_response.json()
                print(f"   User verified: {login_data['user']['is_verified']}")
            else:
                print(f"   ❌ Login failed: {login_response.text}")
        else:
            print(f"   ❌ Registration failed: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_datetime_fix())
