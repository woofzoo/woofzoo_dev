#!/usr/bin/env python3
"""
Test script to verify the login fix works.
"""

import asyncio
import httpx
import json

async def test_login_fix():
    """Test the login fix."""
    
    print("🧪 Testing login fix...")
    
    async with httpx.AsyncClient() as client:
        # Test login
        print("\n1️⃣ Testing login...")
        login_data = {
            "email": "development.woofzoo@gmail.com",
            "password": "Woofzoo123!"
        }
        
        try:
            response = await client.post(
                "http://localhost:8000/api/auth/login",
                json=login_data,
                timeout=10.0
            )
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            if response.status_code == 200:
                print("   ✅ Login successful!")
                login_response = response.json()
                print(f"   User ID: {login_response['user']['id']}")
                print(f"   User Email: {login_response['user']['email']}")
                print(f"   User Verified: {login_response['user']['is_verified']}")
                print(f"   Access Token: {login_response['tokens']['access_token'][:20]}...")
                print(f"   Refresh Token: {login_response['tokens']['refresh_token'][:20]}...")
            else:
                print(f"   ❌ Login failed: {response.text}")
                
        except httpx.ConnectError:
            print("   ❌ Could not connect to server. Make sure it's running on localhost:8000")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_login_fix())
