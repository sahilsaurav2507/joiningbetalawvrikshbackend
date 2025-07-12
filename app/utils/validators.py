"""
Validation utilities for data validation.
"""

import re
from typing import Optional
from email_validator import validate_email as validate_email_format, EmailNotValidError


def validate_email(email: str) -> tuple[bool, Optional[str]]:
    """
    Validate email format and basic structure.
    
    Args:
        email: The email address to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        # Validate email format
        valid = validate_email_format(email)
        email = valid.email
        
        # Additional checks
        if len(email) > 254:  # RFC 5321 limit
            return False, "Email address too long"
        
        if len(email.split('@')[0]) > 64:  # RFC 5321 limit
            return False, "Local part of email too long"
        
        return True, None
        
    except EmailNotValidError as e:
        return False, str(e)


def validate_phone_number(phone: str) -> tuple[bool, Optional[str]]:
    """
    Validate phone number format.
    
    Args:
        phone: The phone number to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check minimum length
    if len(digits_only) < 10:
        return False, "Phone number must contain at least 10 digits"
    
    # Check maximum length
    if len(digits_only) > 15:
        return False, "Phone number too long"
    
    # Basic pattern validation for common formats
    patterns = [
        r'^\+?1?\d{9,15}$',  # International format
        r'^\d{10,15}$',      # National format
    ]
    
    for pattern in patterns:
        if re.match(pattern, digits_only):
            return True, None
    
    return False, "Invalid phone number format"


def validate_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate name format.
    
    Args:
        name: The name to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name.strip()) > 255:
        return False, "Name too long"
    
    # Check for valid characters (letters, spaces, hyphens, apostrophes)
    if not re.match(r'^[a-zA-Z\s\-\'\.]+$', name.strip()):
        return False, "Name contains invalid characters"
    
    return True, None


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS attacks.
    
    Args:
        text: The text to sanitize
        
    Returns:
        str: The sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', 'javascript:', 'onload', 'onerror']
    sanitized = text
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    # Remove script tags
    sanitized = re.sub(r'<script.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    
    return sanitized.strip()


def validate_rating(rating: int, min_rating: int = 1, max_rating: int = 5) -> tuple[bool, Optional[str]]:
    """
    Validate rating value.
    
    Args:
        rating: The rating to validate
        min_rating: Minimum allowed rating
        max_rating: Maximum allowed rating
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(rating, int):
        return False, "Rating must be an integer"
    
    if rating < min_rating or rating > max_rating:
        return False, f"Rating must be between {min_rating} and {max_rating}"
    
    return True, None 