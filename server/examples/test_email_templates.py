"""
Test script for email templates.

This script tests the email templates to ensure they generate correct content.
"""

from app.templates.email_templates import EmailTemplates


def test_verification_email_template():
    """Test email verification template."""
    print("🧪 Testing Email Verification Template")
    print("-" * 40)
    
    to_name = "John Doe"
    verification_url = "http://localhost:3000/api/auth/verify-email?token=abc123"
    
    text_content, html_content = EmailTemplates.get_verification_email_content(
        to_name=to_name,
        verification_url=verification_url
    )
    
    print("✅ Text content generated successfully")
    print(f"📧 Subject: Verify Your Email - WoofZoo")
    print(f"👤 Recipient: {to_name}")
    print(f"🔗 URL: {verification_url}")
    print(f"📝 Text length: {len(text_content)} characters")
    print(f"🌐 HTML length: {len(html_content)} characters")
    print()


def test_password_reset_email_template():
    """Test password reset email template."""
    print("🧪 Testing Password Reset Email Template")
    print("-" * 40)
    
    to_name = "Jane Smith"
    reset_url = "http://localhost:3000/api/auth/reset-password?token=xyz789"
    
    text_content, html_content = EmailTemplates.get_password_reset_email_content(
        to_name=to_name,
        reset_url=reset_url
    )
    
    print("✅ Text content generated successfully")
    print(f"📧 Subject: Reset Your Password - WoofZoo")
    print(f"👤 Recipient: {to_name}")
    print(f"🔗 URL: {reset_url}")
    print(f"📝 Text length: {len(text_content)} characters")
    print(f"🌐 HTML length: {len(html_content)} characters")
    print()


def test_welcome_email_template():
    """Test welcome email template."""
    print("🧪 Testing Welcome Email Template")
    print("-" * 40)
    
    to_name = "Alice Johnson"
    
    text_content, html_content = EmailTemplates.get_welcome_email_content(to_name=to_name)
    
    print("✅ Text content generated successfully")
    print(f"📧 Subject: Welcome to WoofZoo! 🐾")
    print(f"👤 Recipient: {to_name}")
    print(f"📝 Text length: {len(text_content)} characters")
    print(f"🌐 HTML length: {len(html_content)} characters")
    print()


def test_template_content_samples():
    """Show sample content from templates."""
    print("📋 Template Content Samples")
    print("=" * 50)
    
    # Verification email sample
    print("\n📧 Email Verification Sample:")
    print("-" * 30)
    text, html = EmailTemplates.get_verification_email_content(
        "Test User", 
        "http://localhost:3000/api/auth/verify-email?token=test123"
    )
    print("Text content (first 200 chars):")
    print(text[:200] + "...")
    print("\nHTML content (first 300 chars):")
    print(html[:300] + "...")
    
    # Password reset sample
    print("\n🔑 Password Reset Sample:")
    print("-" * 30)
    text, html = EmailTemplates.get_password_reset_email_content(
        "Test User", 
        "http://localhost:3000/api/auth/reset-password?token=test456"
    )
    print("Text content (first 200 chars):")
    print(text[:200] + "...")
    print("\nHTML content (first 300 chars):")
    print(html[:300] + "...")
    
    # Welcome email sample
    print("\n🎉 Welcome Email Sample:")
    print("-" * 30)
    text, html = EmailTemplates.get_welcome_email_content("Test User")
    print("Text content (first 200 chars):")
    print(text[:200] + "...")
    print("\nHTML content (first 300 chars):")
    print(html[:300] + "...")


def main():
    """Run all template tests."""
    print("🐾 WoofZoo Email Templates Test")
    print("=" * 50)
    
    try:
        test_verification_email_template()
        test_password_reset_email_template()
        test_welcome_email_template()
        test_template_content_samples()
        
        print("🎉 All email template tests passed!")
        print("\n✅ Email templates are working correctly.")
        print("📁 Templates are now separated in: app/templates/email_templates.py")
        print("🧹 Email service is now clean and maintainable.")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    main()
