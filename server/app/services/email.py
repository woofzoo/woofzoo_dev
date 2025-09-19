"""
Email service for the application.

This module provides email functionality using SendGrid API for sending
verification emails, password reset emails, and other notifications.
"""

import httpx
from typing import Optional
from datetime import datetime

from app.config import settings
from app.templates.email_templates import EmailTemplates


class EmailService:
    """
    Email service for sending emails via SendGrid API.
    
    This class handles all email operations including verification emails,
    password reset emails, and other notifications.
    """
    
    def __init__(self) -> None:
        """Initialize the email service."""
        self.api_key = settings.sendgrid_api_key
        self.from_email = settings.email_from_address
        self.from_name = settings.email_from_name
        self.base_url = "https://api.sendgrid.com/v3"
        self.frontend_url = settings.frontend_url
    
    def send_email(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        text_content: str,
        html_content: Optional[str] = None
    ) -> bool:
        """
        Send an email via SendGrid API.
        
        Args:
            to_email: Recipient email address
            to_name: Recipient name
            subject: Email subject
            text_content: Plain text content
            html_content: HTML content (optional)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        # In debug mode, just log the email instead of sending
        if settings.debug:
            print(f"🔧 DEBUG MODE - Email would be sent:")
            print(f"   To: {to_name} <{to_email}>")
            print(f"   Subject: {subject}")
            print(f"   Content: {text_content[:100]}...")
            if html_content:
                print(f"   HTML Content: {html_content[:100]}...")
            return True
        
        try:
        
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            body = {
                "personalizations": [
                    {
                        "to": [{"email": to_email, "name": to_name}],
                    }
                ],
                "from": {"email": self.from_email, "name": self.from_name},
                "subject": subject,
                "content": [
                    {"type": "text/plain", "value": text_content}
                ],
            }
            if html_content:
                body["content"].append({"type": "text/html", "value": html_content})

            with httpx.Client() as client:
                response = client.post(
                    f"{self.base_url}/mail/send",
                    headers=headers,
                    json=body,
                    timeout=30.0,
                )
                
                if response.status_code in (200, 202):
                    return True
                else:
                    print(f"Failed to send email: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def send_verification_email(self, to_email: str, to_name: str, token: str) -> bool:
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
        
        return self.send_email(to_email, to_name, subject, text_content, html_content)
    
    def send_password_reset_email(self, to_email: str, to_name: str, token: str) -> bool:
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
        
        return self.send_email(to_email, to_name, subject, text_content, html_content)
    
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
        
        return self.send_email(to_email, to_name, subject, text_content, html_content)
