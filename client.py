"""
Distributed Task Scheduler Client

A simple CLI client for submitting tasks to the distributed task scheduler.
"""

import asyncio
import sys
import uuid
import logging
from typing import Dict, Any
from server import TASK_QUEUE

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def submit_task(data: str) -> Dict[str, Any]:
    """
    Submit a task to the scheduler.
    
    Args:
        data: The string data to hash
        
    Returns:
        The submitted task dictionary
    """
    task = {"id": str(uuid.uuid4()), "data": data}
    await TASK_QUEUE.put(task)
    logger.info(f"Submitted task: {task['id']}")
    return task

def print_usage() -> None:
    """Print usage instructions."""
    print("Usage: python client.py <string_to_hash>")
    print("Example: python client.py 'Hello, World!'")

async def main() -> None:
    """Main client function."""
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)
        
    data = sys.argv[1]
    if not data.strip():
        print("Error: Empty string provided")
        print_usage()
        sys.exit(1)
        
    try:
        await submit_task(data)
        print(f"Task submitted successfully for string: '{data}'")
    except Exception as e:
        logger.error(f"Failed to submit task: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
