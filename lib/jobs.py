"""
Task Processing Functions

Contains the actual task processing logic for the distributed scheduler.
"""

import hashlib

def hash_string(data: str) -> str:
    """
    Compute SHA256 hash of a string.
    
    Args:
        data: String to hash
        
    Returns:
        Hexadecimal representation of the SHA256 hash
        
    Raises:
        TypeError: If data is not a string
    """
    if not isinstance(data, str):
        raise TypeError("Data must be a string")
        
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
