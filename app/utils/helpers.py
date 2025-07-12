"""
Helper utility functions for common operations.
"""

import uuid
from datetime import datetime
from typing import Optional
import math


def generate_session_id() -> str:
    """
    Generate a unique session ID for feedback sessions.
    
    Returns:
        str: A unique session ID
    """
    return str(uuid.uuid4())


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object to string.
    
    Args:
        dt: The datetime object to format
        format_str: The format string to use
        
    Returns:
        str: The formatted datetime string
    """
    return dt.strftime(format_str)


def calculate_pagination(total: int, page: int, size: int) -> dict:
    """
    Calculate pagination information.
    
    Args:
        total: Total number of items
        page: Current page number
        size: Items per page
        
    Returns:
        dict: Pagination information
    """
    total_pages = math.ceil(total / size) if total > 0 else 0
    offset = (page - 1) * size
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "pages": total_pages,
        "offset": offset,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename for safe file operations.
    
    Args:
        filename: The filename to sanitize
        
    Returns:
        str: The sanitized filename
    """
    import re
    # Remove or replace dangerous characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    # Limit length
    if len(sanitized) > 255:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        sanitized = name[:255-len(ext)-1] + ('.' + ext if ext else '')
    
    return sanitized or "unnamed_file"


def generate_export_filename(prefix: str = "export", extension: str = "xlsx") -> str:
    """
    Generate a filename for data exports.
    
    Args:
        prefix: The filename prefix
        extension: The file extension
        
    Returns:
        str: The generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: The text to truncate
        max_length: Maximum length allowed
        suffix: Suffix to add when truncated
        
    Returns:
        str: The truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_phone_number(phone: str) -> str:
    """
    Format phone number for display.
    
    Args:
        phone: The phone number to format
        
    Returns:
        str: The formatted phone number
    """
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format


def mask_email(email: str) -> str:
    """
    Mask an email address for privacy.
    
    Args:
        email: The email address to mask
        
    Returns:
        str: The masked email address
    """
    if '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    
    if len(local) <= 2:
        masked_local = local
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    
    return f"{masked_local}@{domain}"


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """
    Validate file extension.
    
    Args:
        filename: The filename to validate
        allowed_extensions: List of allowed extensions
        
    Returns:
        bool: True if extension is allowed, False otherwise
    """
    if not filename:
        return False
    
    file_extension = filename.lower().split('.')[-1] if '.' in filename else ''
    return file_extension in [ext.lower() for ext in allowed_extensions]


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS and other injection attacks.
    
    Args:
        text: The text to sanitize
        
    Returns:
        str: The sanitized text
    """
    if not text:
        return ""
    
    import re
    import html
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove or escape potentially dangerous characters
    # Remove script tags and their content
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove other potentially dangerous HTML tags
    dangerous_tags = ['iframe', 'object', 'embed', 'form', 'input', 'textarea', 'select', 'button']
    for tag in dangerous_tags:
        text = re.sub(r'<' + tag + r'[^>]*>.*?</' + tag + r'>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<' + tag + r'[^>]*/?>', '', text, flags=re.IGNORECASE)
    
    # Remove JavaScript event handlers
    text = re.sub(r'\bon\w+\s*=', '', text, flags=re.IGNORECASE)
    
    # Remove SQL injection patterns
    sql_patterns = [
        r'(\b(union|select|insert|update|delete|drop|create|alter)\b)',
        r'(\b(and|or)\b\s+\d+\s*=\s*\d+)',
        r'(\b(and|or)\b\s+\'\w+\'\s*=\s*\'\w+\')',
        r'(\b(and|or)\b\s+\"\w+\"\s*=\s*\"\w+\")',
        r'(\b(and|or)\b\s+\w+\s*=\s*\w+)',
    ]
    
    for pattern in sql_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove multiple spaces and normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace
    text = text.strip()
    
    # Limit length to prevent buffer overflow attacks
    max_length = 1000
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def sanitize_email(email: str) -> str:
    """
    Sanitize email address.
    
    Args:
        email: The email to sanitize
        
    Returns:
        str: The sanitized email
    """
    if not email:
        return ""
    
    # Convert to lowercase and strip whitespace
    email = email.lower().strip()
    
    # Basic email validation
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format")
    
    return email


def sanitize_phone_number(phone: str) -> str:
    """
    Sanitize phone number.
    
    Args:
        phone: The phone number to sanitize
        
    Returns:
        str: The sanitized phone number
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters except + for international numbers
    import re
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Remove multiple + signs
    phone = re.sub(r'\++', '+', phone)
    
    # Ensure only one + at the beginning
    if phone.startswith('+'):
        phone = '+' + phone[1:].replace('+', '')
    
    # Basic validation
    if len(phone) < 10 or len(phone) > 15:
        raise ValueError("Invalid phone number length")
    
    return phone 