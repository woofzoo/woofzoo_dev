"""
Email templates for the application.

This module contains all email templates for verification, password reset,
and welcome emails in both HTML and plain text formats.
"""

from typing import Optional
from app.config import settings


class EmailTemplates:
    """Email templates for various types of emails."""
    
    @staticmethod
    def get_verification_email_content(to_name: str, verification_url: str) -> tuple[str, str]:
        """
        Get email verification email content.
        
        Args:
            to_name: Recipient name
            verification_url: Email verification URL
            
        Returns:
            tuple[str, str]: (text_content, html_content)
        """
        text_content = f"""
Hello {to_name},

Thank you for signing up with WoofZoo! Please verify your email address by clicking the link below:

{verification_url}

This link will expire in {settings.email_verification_expire_hours} hours.

If you didn't create an account with WoofZoo, please ignore this email.

Best regards,
The WoofZoo Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Verify Your Email - WoofZoo</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .button {{ display: inline-block; padding: 12px 24px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐾 WoofZoo</h1>
        </div>
        <div class="content">
            <h2>Hello {to_name}!</h2>
            <p>Thank you for signing up with WoofZoo! Please verify your email address by clicking the button below:</p>
            
            <div style="text-align: center;">
                <a href="{verification_url}" class="button">Verify Email Address</a>
            </div>
            
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #666;">{verification_url}</p>
            
            <p><strong>This link will expire in {settings.email_verification_expire_hours} hours.</strong></p>
            
            <p>If you didn't create an account with WoofZoo, please ignore this email.</p>
        </div>
        <div class="footer">
            <p>Best regards,<br>The WoofZoo Team</p>
        </div>
    </div>
</body>
</html>
        """
        
        return text_content.strip(), html_content.strip()
    
    @staticmethod
    def get_family_invitation_email_content(to_name: str, family_name: str, inviter_name: str, invitation_url: str, message: Optional[str] = None) -> tuple[str, str]:
        """
        Get family invitation email content.
        
        Args:
            to_name: Recipient name
            family_name: Name of the family
            inviter_name: Name of the person who sent the invitation
            invitation_url: Family invitation URL
            message: Optional invitation message
            
        Returns:
            tuple[str, str]: (text_content, html_content)
        """
        text_content = f"""
Hello {to_name},

{inviter_name} has invited you to join the {family_name} on WoofZoo!

{f"Message from {inviter_name}: {message}" if message else ""}

To accept this invitation and help manage the family's pets, click the link below:

{invitation_url}

This invitation will expire in 7 days.

If you don't want to accept this invitation, you can simply ignore this email.

Best regards,
The WoofZoo Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Family Invitation - WoofZoo</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .invitation-box {{ margin: 20px 0; padding: 20px; background-color: white; border-radius: 5px; border-left: 4px solid #4CAF50; }}
        .cta-button {{ display: inline-block; padding: 12px 24px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .message-box {{ margin: 15px 0; padding: 15px; background-color: #e8f5e8; border-radius: 5px; font-style: italic; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐾 Family Invitation</h1>
        </div>
        <div class="content">
            <h2>Hello {to_name}!</h2>
            
            <div class="invitation-box">
                <h3>You're invited to join {family_name}!</h3>
                <p><strong>{inviter_name}</strong> has invited you to join their family on WoofZoo to help manage their pets.</p>
                
                {f'<div class="message-box"><strong>Message from {inviter_name}:</strong><br>"{message}"</div>' if message else ''}
                
                <p>As a family member, you'll be able to:</p>
                <ul>
                    <li>🐕 View and manage pet health records</li>
                    <li>📅 Schedule veterinary appointments</li>
                    <li>💉 Track vaccinations and medications</li>
                    <li>👨‍👩‍👧‍👦 Coordinate care with other family members</li>
                </ul>
                
                <a href="{invitation_url}" class="cta-button">Accept Invitation</a>
            </div>
            
            <p><small>This invitation will expire in 7 days. If you don't want to accept this invitation, you can simply ignore this email.</small></p>
        </div>
        <div class="footer">
            <p>Best regards,<br>The WoofZoo Team</p>
        </div>
    </div>
</body>
</html>
        """
        
        return text_content.strip(), html_content.strip()
    
    @staticmethod
    def get_password_reset_email_content(to_name: str, reset_url: str) -> tuple[str, str]:
        """
        Get password reset email content.
        
        Args:
            to_name: Recipient name
            reset_url: Password reset URL
            
        Returns:
            tuple[str, str]: (text_content, html_content)
        """
        text_content = f"""
Hello {to_name},

You requested to reset your password for your WoofZoo account. Click the link below to reset your password:

{reset_url}

This link will expire in {settings.password_reset_expire_hours} hours.

If you didn't request a password reset, please ignore this email. Your password will remain unchanged.

Best regards,
The WoofZoo Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Reset Your Password - WoofZoo</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #FF6B6B; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .button {{ display: inline-block; padding: 12px 24px; background-color: #FF6B6B; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        .warning {{ background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐾 WoofZoo</h1>
        </div>
        <div class="content">
            <h2>Hello {to_name}!</h2>
            <p>You requested to reset your password for your WoofZoo account. Click the button below to reset your password:</p>
            
            <div style="text-align: center;">
                <a href="{reset_url}" class="button">Reset Password</a>
            </div>
            
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #666;">{reset_url}</p>
            
            <div class="warning">
                <p><strong>This link will expire in {settings.password_reset_expire_hours} hours.</strong></p>
                <p>If you didn't request a password reset, please ignore this email. Your password will remain unchanged.</p>
            </div>
        </div>
        <div class="footer">
            <p>Best regards,<br>The WoofZoo Team</p>
        </div>
    </div>
</body>
</html>
        """
        
        return text_content.strip(), html_content.strip()
    
    @staticmethod
    def get_family_invitation_email_content(to_name: str, family_name: str, inviter_name: str, invitation_url: str, message: Optional[str] = None) -> tuple[str, str]:
        """
        Get family invitation email content.
        
        Args:
            to_name: Recipient name
            family_name: Name of the family
            inviter_name: Name of the person who sent the invitation
            invitation_url: Family invitation URL
            message: Optional invitation message
            
        Returns:
            tuple[str, str]: (text_content, html_content)
        """
        text_content = f"""
Hello {to_name},

{inviter_name} has invited you to join the {family_name} on WoofZoo!

{f"Message from {inviter_name}: {message}" if message else ""}

To accept this invitation and help manage the family's pets, click the link below:

{invitation_url}

This invitation will expire in 7 days.

If you don't want to accept this invitation, you can simply ignore this email.

Best regards,
The WoofZoo Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Family Invitation - WoofZoo</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .invitation-box {{ margin: 20px 0; padding: 20px; background-color: white; border-radius: 5px; border-left: 4px solid #4CAF50; }}
        .cta-button {{ display: inline-block; padding: 12px 24px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .message-box {{ margin: 15px 0; padding: 15px; background-color: #e8f5e8; border-radius: 5px; font-style: italic; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐾 Family Invitation</h1>
        </div>
        <div class="content">
            <h2>Hello {to_name}!</h2>
            
            <div class="invitation-box">
                <h3>You're invited to join {family_name}!</h3>
                <p><strong>{inviter_name}</strong> has invited you to join their family on WoofZoo to help manage their pets.</p>
                
                {f'<div class="message-box"><strong>Message from {inviter_name}:</strong><br>"{message}"</div>' if message else ''}
                
                <p>As a family member, you'll be able to:</p>
                <ul>
                    <li>🐕 View and manage pet health records</li>
                    <li>📅 Schedule veterinary appointments</li>
                    <li>💉 Track vaccinations and medications</li>
                    <li>👨‍👩‍👧‍👦 Coordinate care with other family members</li>
                </ul>
                
                <a href="{invitation_url}" class="cta-button">Accept Invitation</a>
            </div>
            
            <p><small>This invitation will expire in 7 days. If you don't want to accept this invitation, you can simply ignore this email.</small></p>
        </div>
        <div class="footer">
            <p>Best regards,<br>The WoofZoo Team</p>
        </div>
    </div>
</body>
</html>
        """
        
        return text_content.strip(), html_content.strip()
    
    @staticmethod
    def get_welcome_email_content(to_name: str) -> tuple[str, str]:
        """
        Get welcome email content.
        
        Args:
            to_name: Recipient name
            
        Returns:
            tuple[str, str]: (text_content, html_content)
        """
        text_content = f"""
Hello {to_name},

Welcome to WoofZoo! We're excited to have you on board.

WoofZoo is your comprehensive platform for pet care management, connecting pet owners with veterinary clinics and providing a seamless experience for all your pet care needs.

Here's what you can do with WoofZoo:
• Manage your pet's health records
• Schedule appointments with veterinary clinics
• Track vaccinations and medications
• Connect with family members for pet care coordination
• Access professional veterinary services

If you have any questions or need assistance, please don't hesitate to contact our support team.

Best regards,
The WoofZoo Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Welcome to WoofZoo!</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .feature {{ margin: 10px 0; padding: 10px; background-color: white; border-radius: 5px; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐾 Welcome to WoofZoo!</h1>
        </div>
        <div class="content">
            <h2>Hello {to_name}!</h2>
            <p>Welcome to WoofZoo! We're excited to have you on board.</p>
            
            <p>WoofZoo is your comprehensive platform for pet care management, connecting pet owners with veterinary clinics and providing a seamless experience for all your pet care needs.</p>
            
            <h3>Here's what you can do with WoofZoo:</h3>
            <div class="feature">🐕 Manage your pet's health records</div>
            <div class="feature">📅 Schedule appointments with veterinary clinics</div>
            <div class="feature">💉 Track vaccinations and medications</div>
            <div class="feature">👨‍👩‍👧‍👦 Connect with family members for pet care coordination</div>
            <div class="feature">🏥 Access professional veterinary services</div>
            
            <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>
        </div>
        <div class="footer">
            <p>Best regards,<br>The WoofZoo Team</p>
        </div>
    </div>
</body>
</html>
        """
        
        return text_content.strip(), html_content.strip()
    
    @staticmethod
    def get_family_invitation_email_content(to_name: str, family_name: str, inviter_name: str, invitation_url: str, message: Optional[str] = None) -> tuple[str, str]:
        """
        Get family invitation email content.
        
        Args:
            to_name: Recipient name
            family_name: Name of the family
            inviter_name: Name of the person who sent the invitation
            invitation_url: Family invitation URL
            message: Optional invitation message
            
        Returns:
            tuple[str, str]: (text_content, html_content)
        """
        text_content = f"""
Hello {to_name},

{inviter_name} has invited you to join the {family_name} on WoofZoo!

{f"Message from {inviter_name}: {message}" if message else ""}

To accept this invitation and help manage the family's pets, click the link below:

{invitation_url}

This invitation will expire in 7 days.

If you don't want to accept this invitation, you can simply ignore this email.

Best regards,
The WoofZoo Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Family Invitation - WoofZoo</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .invitation-box {{ margin: 20px 0; padding: 20px; background-color: white; border-radius: 5px; border-left: 4px solid #4CAF50; }}
        .cta-button {{ display: inline-block; padding: 12px 24px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .message-box {{ margin: 15px 0; padding: 15px; background-color: #e8f5e8; border-radius: 5px; font-style: italic; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐾 Family Invitation</h1>
        </div>
        <div class="content">
            <h2>Hello {to_name}!</h2>
            
            <div class="invitation-box">
                <h3>You're invited to join {family_name}!</h3>
                <p><strong>{inviter_name}</strong> has invited you to join their family on WoofZoo to help manage their pets.</p>
                
                {f'<div class="message-box"><strong>Message from {inviter_name}:</strong><br>"{message}"</div>' if message else ''}
                
                <p>As a family member, you'll be able to:</p>
                <ul>
                    <li>🐕 View and manage pet health records</li>
                    <li>📅 Schedule veterinary appointments</li>
                    <li>💉 Track vaccinations and medications</li>
                    <li>👨‍👩‍👧‍👦 Coordinate care with other family members</li>
                </ul>
                
                <a href="{invitation_url}" class="cta-button">Accept Invitation</a>
            </div>
            
            <p><small>This invitation will expire in 7 days. If you don't want to accept this invitation, you can simply ignore this email.</small></p>
        </div>
        <div class="footer">
            <p>Best regards,<br>The WoofZoo Team</p>
        </div>
    </div>
</body>
</html>
        """
        
        return text_content.strip(), html_content.strip()
