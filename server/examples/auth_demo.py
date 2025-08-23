"""
Authentication System Demo

This script demonstrates the usage of the WoofZoo authentication system
by creating a user, logging in, and performing various operations.
"""

import asyncio
import httpx
import json
from typing import Dict, Any


class AuthDemo:
    """Demo class for authentication system."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the demo with base URL."""
        self.base_url = base_url
        self.client = httpx.AsyncClient()
        self.access_token = None
        self.refresh_token = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.aclose()
    
    async def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new user."""
        print(f"🔐 Registering user: {user_data['email']}")
        
        response = await self.client.post(
            f"{self.base_url}/api/auth/register",
            json=user_data
        )
        
        if response.status_code == 201:
            print("✅ User registered successfully")
            return response.json()
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
    
    async def login_user(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """Login user and get tokens."""
        print(f"🔑 Logging in user: {credentials['email']}")
        
        response = await self.client.post(
            f"{self.base_url}/api/auth/login",
            json=credentials
        )
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["tokens"]["access_token"]
            self.refresh_token = data["tokens"]["refresh_token"]
            print("✅ Login successful")
            print(f"User: {data['user']['first_name']} {data['user']['last_name']}")
            print(f"Roles: {data['user']['roles']}")
            return data
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
    
    async def get_current_user(self) -> Dict[str, Any]:
        """Get current user information."""
        if not self.access_token:
            print("❌ No access token available")
            return None
        
        print("👤 Getting current user information")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = await self.client.get(
            f"{self.base_url}/api/auth/me",
            headers=headers
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Current user retrieved")
            print(f"Email: {user_data['email']}")
            print(f"Verified: {user_data['is_verified']}")
            print(f"Personalization: {user_data['personalization']}")
            return user_data
        else:
            print(f"❌ Failed to get current user: {response.status_code}")
            print(f"Error: {response.text}")
            return None
    
    async def update_personalization(self, personalization: Dict[str, Any]) -> Dict[str, Any]:
        """Update user personalization settings."""
        if not self.access_token:
            print("❌ No access token available")
            return None
        
        print("🎨 Updating personalization settings")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = await self.client.put(
            f"{self.base_url}/api/auth/me/personalization",
            json={"personalization": personalization},
            headers=headers
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Personalization updated")
            print(f"New settings: {user_data['personalization']}")
            return user_data
        else:
            print(f"❌ Failed to update personalization: {response.status_code}")
            print(f"Error: {response.text}")
            return None
    
    async def refresh_tokens(self) -> Dict[str, Any]:
        """Refresh access token."""
        if not self.refresh_token:
            print("❌ No refresh token available")
            return None
        
        print("🔄 Refreshing tokens")
        
        response = await self.client.post(
            f"{self.base_url}/api/auth/refresh",
            params={"refresh_token": self.refresh_token}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            self.refresh_token = data["refresh_token"]
            print("✅ Tokens refreshed successfully")
            return data
        else:
            print(f"❌ Token refresh failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
    
    async def request_password_reset(self, email: str) -> bool:
        """Request password reset."""
        print(f"📧 Requesting password reset for: {email}")
        
        response = await self.client.post(
            f"{self.base_url}/api/auth/request-password-reset",
            json={"email": email}
        )
        
        if response.status_code == 200:
            print("✅ Password reset email sent")
            return True
        else:
            print(f"❌ Password reset request failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    
    async def logout(self) -> bool:
        """Logout user."""
        if not self.access_token:
            print("❌ No access token available")
            return False
        
        print("🚪 Logging out")
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = await self.client.post(
            f"{self.base_url}/api/auth/logout",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Logout successful")
            self.access_token = None
            self.refresh_token = None
            return True
        else:
            print(f"❌ Logout failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False


async def main():
    """Main demo function."""
    print("🐾 WoofZoo Authentication System Demo")
    print("=" * 50)
    
    # Demo user data
    user_data = {
        "email": "demo@woofzoo.com",
        "first_name": "Demo",
        "last_name": "User",
        "phone": "+1234567890",
        "password": "SecurePass123!",
        "roles": ["pet_owner", "clinic_owner"]
    }
    
    credentials = {
        "email": "demo@woofzoo.com",
        "password": "SecurePass123!"
    }
    
    async with AuthDemo() as demo:
        # Step 1: Register a new user
        print("\n1️⃣ User Registration")
        print("-" * 30)
        await demo.register_user(user_data)
        
        # Step 2: Login user
        print("\n2️⃣ User Login")
        print("-" * 30)
        await demo.login_user(credentials)
        
        # Step 3: Get current user
        print("\n3️⃣ Get Current User")
        print("-" * 30)
        await demo.get_current_user()
        
        # Step 4: Update personalization
        print("\n4️⃣ Update Personalization")
        print("-" * 30)
        personalization = {
            "theme": "dark",
            "language": "en",
            "notifications": {
                "email": True,
                "push": False
            },
            "preferences": {
                "timezone": "UTC",
                "currency": "USD"
            }
        }
        await demo.update_personalization(personalization)
        
        # Step 5: Refresh tokens
        print("\n5️⃣ Token Refresh")
        print("-" * 30)
        await demo.refresh_tokens()
        
        # Step 6: Request password reset
        print("\n6️⃣ Password Reset Request")
        print("-" * 30)
        await demo.request_password_reset(user_data["email"])
        
        # Step 7: Logout
        print("\n7️⃣ User Logout")
        print("-" * 30)
        await demo.logout()
        
        # Step 8: Try to access protected endpoint after logout
        print("\n8️⃣ Access After Logout")
        print("-" * 30)
        await demo.get_current_user()
    
    print("\n🎉 Demo completed!")
    print("\n📚 Next steps:")
    print("1. Check your email for verification link")
    print("2. Verify your email address")
    print("3. Try logging in again")
    print("4. Explore the API documentation at http://localhost:8000/docs")


if __name__ == "__main__":
    asyncio.run(main())
