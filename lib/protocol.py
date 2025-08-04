"""
Custom Binary RPC Protocol

A simple binary protocol for communication between scheduler and workers.
Message format: [1 byte command][4 bytes length][payload]
"""

import struct
from typing import Tuple, Optional, Union

HEADER_FMT = '!BI'  # Big-endian: 1 byte unsigned char + 4 bytes unsigned int
HEADER_SIZE = struct.calcsize(HEADER_FMT)

def encode_message(command: int, payload: bytes) -> bytes:
    """
    Encode a message with command and payload.
    
    Args:
        command: Command identifier (1 byte)
        payload: Message payload as bytes
        
    Returns:
        Encoded message as bytes
        
    Raises:
        ValueError: If command is not in valid range (0-255)
    """
    if not 0 <= command <= 255:
        raise ValueError("Command must be between 0 and 255")
        
    if len(payload) > 0xFFFFFFFF:
        raise ValueError("Payload too large (max 4GB)")
        
    header = struct.pack(HEADER_FMT, command, len(payload))
    return header + payload

def decode_message(buffer: bytes) -> Tuple[Optional[Tuple[int, bytes]], bytes]:
    """
    Decode a message from buffer.
    
    Args:
        buffer: Raw bytes buffer
        
    Returns:
        Tuple of (decoded_message, remaining_buffer)
        decoded_message is None if not enough data
    """
    if len(buffer) < HEADER_SIZE:
        return None, buffer
        
    try:
        command, length = struct.unpack(HEADER_FMT, buffer[:HEADER_SIZE])
    except struct.error:
        return None, buffer
        
    if len(buffer) < HEADER_SIZE + length:
        return None, buffer
        
    payload = buffer[HEADER_SIZE:HEADER_SIZE + length]
    return (command, payload), buffer[HEADER_SIZE + length:]
