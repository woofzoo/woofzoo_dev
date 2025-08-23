"""
Email service for the application.

This module provides email functionality using Mailgun API for sending
verification emails, password reset emails, and other notifications.
"""

import httpx
from typing import Optional
from datetime import datetime

from app.config import settings
from app.templates.email_templates import EmailTemplates


class EmailService:
    """
    Email service for sending emails via Mailgun API.
    
    This class handles all email operations including verification emails,
    password reset emails, and other notifications.
    """
    
    def __init__(self) -> None:
        """Initialize the email service."""
        self.api_key = settings.mailgun_api_key
        self.domain = settings.mailgun_domain
        self.from_email = settings.mailgun_from_email
        self.from_name = settings.mailgun_from_name
        self.base_url = f"https://api.mailgun.net/v3/{self.domain}"
        self.frontend_url = settings.frontend_url
    
    async def send_email(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        text_content: str,
        html_content: Optional[str] = None
    ) -> bool:
        """
        Send an email via Mailgun API.
        
        Args:
            to_email: Recipient email address
            to_name: Recipient name
            subject: Email subject
            text_content: Plain text content
            html_content: HTML content (optional)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    "from": f"{self.from_name} <{self.from_email}>",
                    "to": f"{to_name} <{to_email}>",
                    "subject": subject,
                    "text": text_content
                }
                
                if html_content:
                    data["html"] = html_content
                
                response = await client.post(
                    f"{self.base_url}/messages",
                    data=data,
                    auth=("api", self.api_key),
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return True
                else:
                    print(f"Failed to send email: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    async def send_verification_email(self, to_email: str, to_name: str, token: str) -> bool:
        """
        Send email verification email.
        
        Args:
            to_email: Recipient email address
            to_name: Recipient name
            token: Verification token
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        # Use GET endpoint for direct verification from email link
        verification_url = f"{self.frontend_url}/api/auth/verify-email?token={token}"
        
        # Get email content from templates
        text_content, html_content = EmailTemplates.get_verification_email_content(
            to_name=to_name,
            verification_url=verification_url
        )
        
        subject = "Verify Your Email - WoofZoo"
        
        return await self.send_email(to_email, to_name, subject, text_content, html_content)
    
    async def send_password_reset_email(self, to_email: str, to_name: str, token: str) -> bool:
        """
        Send password reset email.
        
        Args:
            to_email: Recipient email address
            to_name: Recipient name
            token: Password reset token
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        # Use GET endpoint to redirect to frontend reset form
        reset_url = f"{self.frontend_url}/api/auth/reset-password?token={token}"
        
        # Get email content from templates
        text_content, html_content = EmailTemplates.get_password_reset_email_content(
            to_name=to_name,
            reset_url=reset_url
        )
        
        subject = "Reset Your Password - WoofZoo"
        
        return await self.send_email(to_email, to_name, subject, text_content, html_content)
    
    async def send_welcome_email(self, to_email: str, to_name: str) -> bool:
        """
        Send welcome email to new users.
        
        Args:
            to_email: Recipient email address
            to_name: Recipient name
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        # Get email content from templates
        text_content, html_content = EmailTemplates.get_welcome_email_content(to_name=to_name)
        
        subject = "Welcome to WoofZoo! 🐾"
        
        return await self.send_email(to_email, to_name, subject, text_content, html_content)
