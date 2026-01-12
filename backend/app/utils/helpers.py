"""
Helper Functions
General utility functions
"""
import uuid
from datetime import datetime
from typing import Optional


def generate_uuid() -> str:
    """Generate a new UUID"""
    return str(uuid.uuid4())


def get_current_timestamp() -> datetime:
    """Get current UTC timestamp"""
    return datetime.utcnow()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove special characters and spaces
    import re
    filename = re.sub(r'[^\w\s.-]', '', filename)
    filename = filename.replace(' ', '_')
    
    # Add timestamp to make unique
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    
    return f"{name}_{timestamp}.{ext}" if ext else f"{name}_{timestamp}"


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_file_extension(filename: str) -> Optional[str]:
    """
    Get file extension from filename
    
    Args:
        filename: Filename
    
    Returns:
        File extension or None
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return None
