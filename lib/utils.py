"""
Utility Functions

Helper functions for the distributed task scheduler.
"""

import asyncio

async def read_exactly(reader: asyncio.StreamReader, n: int) -> bytes:
    """
    Read exactly n bytes from a stream reader.
    
    Args:
        reader: Async stream reader
        n: Number of bytes to read
        
    Returns:
        Exactly n bytes from the stream
        
    Raises:
        ConnectionError: If connection is closed before reading n bytes
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Cannot read negative number of bytes")
        
    data = b''
    while len(data) < n:
        packet = await reader.read(n - len(data))
        if not packet:
            raise ConnectionError("Connection closed before reading complete data")
        data += packet
    return data
