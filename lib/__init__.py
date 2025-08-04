"""
Distributed Task Scheduler Library

A collection of utilities and protocols for the distributed task scheduler.
"""

__version__ = "0.1.0"
__author__ = "Ray"
__email__ = ray@venterprise.io"

from .protocol import encode_message, decode_message
from .jobs import hash_string
from .utils import read_exactly

__all__ = [
    "encode_message",
    "decode_message", 
    "hash_string",
    "read_exactly",
] 