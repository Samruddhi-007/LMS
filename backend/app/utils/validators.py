"""
Custom Validators
Validation utilities for data validation
"""
import re
from typing import Optional


def validate_pin_code(pin_code: str) -> bool:
    """
    Validate Indian PIN code (6 digits)
    
    Args:
        pin_code: PIN code to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^\d{6}$'
    return bool(re.match(pattern, pin_code))


def validate_mobile_number(mobile: str) -> bool:
    """
    Validate Indian mobile number
    
    Args:
        mobile: Mobile number to validate
    
    Returns:
        True if valid, False otherwise
    """
    # Remove spaces and special characters
    cleaned = re.sub(r'[^\d+]', '', mobile)
    
    # Check for Indian mobile number patterns
    patterns = [
        r'^\+91\d{10}$',  # +91XXXXXXXXXX
        r'^91\d{10}$',    # 91XXXXXXXXXX
        r'^\d{10}$'       # XXXXXXXXXX
    ]
    
    return any(re.match(pattern, cleaned) for pattern in patterns)


def validate_ifsc_code(ifsc: str) -> bool:
    """
    Validate IFSC code
    
    Args:
        ifsc: IFSC code to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
    return bool(re.match(pattern, ifsc.upper()))


def validate_gst_number(gst: str) -> bool:
    """
    Validate GST number
    
    Args:
        gst: GST number to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$'
    return bool(re.match(pattern, gst.upper()))


def validate_coordinates(latitude: Optional[str], longitude: Optional[str]) -> bool:
    """
    Validate GPS coordinates
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
    
    Returns:
        True if valid, False otherwise
    """
    if not latitude or not longitude:
        return False
    
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        # Check valid ranges
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return True
    except ValueError:
        pass
    
    return False
