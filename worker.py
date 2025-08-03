"""
Distributed Task Scheduler Worker

A worker process that connects to the scheduler and processes
SHA256 hashing tasks using a custom binary RPC protocol.
"""

import asyncio
import json
import logging
from typing import Dict, Any
from lib.protocol import decode_message, encode_message
from lib.jobs import hash_string
from lib.utils import read_exactly

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Protocol constants
COMMAND_TASK = 1
COMMAND_RESULT = 2
COMMAND_HELLO = 3

async def main() -> None:
    """Connect to scheduler and process tasks."""
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 9001)
        logger.info("Connected to scheduler")
        
        while True:
            try:
                # Read message header (5 bytes: 1 byte command + 4 bytes length)
                header = await read_exactly(reader, 5)
                (cmd, length), _ = decode_message(header + await read_exactly(reader, length))
                
                if cmd == COMMAND_TASK:
                    task = json.loads(_)
                    logger.info(f"Processing task {task['id']}")
                    
                    # Process the task
                    result = hash_string(task['data'])
                    
                    # Send result back to scheduler
                    response = {
                        "task_id": task['id'],
                        "result": result
                    }
                    msg = encode_message(COMMAND_RESULT, json.dumps(response).encode())
                    writer.write(msg)
                    await writer.drain()
                    logger.info(f"Completed task {task['id']}")
                    
            except Exception as e:
                logger.error(f"Error processing task: {e}")
                break
                
    except Exception as e:
        logger.error(f"Failed to connect to scheduler: {e}")
    finally:
        if 'writer' in locals():
            writer.close()
            await writer.wait_closed()
        logger.info("Worker stopped")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker stopped by user")
