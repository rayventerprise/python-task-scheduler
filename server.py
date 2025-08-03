"""
Distributed Task Scheduler Server

A low-level, asyncio-based task scheduler that coordinates workers
to process tasks via a custom binary RPC protocol over TCP.
"""

import asyncio
import json
import logging
from typing import Set, Tuple, Dict, Any
from lib.protocol import encode_message, decode_message
from lib.jobs import hash_string
from lib.utils import read_exactly

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global state
WORKERS: Set[Tuple[asyncio.StreamReader, asyncio.StreamWriter]] = set()
TASK_QUEUE: asyncio.Queue = asyncio.Queue()
RESULTS: Dict[str, Any] = {}

# Protocol constants
COMMAND_TASK = 1
COMMAND_RESULT = 2
COMMAND_HELLO = 3

async def handle_worker(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    """
    Handle a worker connection.
    
    Args:
        reader: Stream reader for receiving data from worker
        writer: Stream writer for sending data to worker
    """
    addr = writer.get_extra_info("peername")
    logger.info(f"Worker connected: {addr}")
    WORKERS.add((reader, writer))
    
    try:
        while True:
            # Read message header (5 bytes: 1 byte command + 4 bytes length)
            header = await read_exactly(reader, 5)
            (cmd, length), _ = decode_message(header + await read_exactly(reader, length))
            
            if cmd == COMMAND_RESULT:
                result = json.loads(_)
                RESULTS[result['task_id']] = result['result']
                logger.info(f"Received result for task {result['task_id']}")
                
    except Exception as e:
        logger.error(f"Worker {addr} disconnected: {e}")
    finally:
        WORKERS.remove((reader, writer))
        writer.close()
        await writer.wait_closed()
        logger.info(f"Worker {addr} disconnected")

async def assign_tasks() -> None:
    """Continuously assign tasks from the queue to available workers."""
    while True:
        try:
            task = await TASK_QUEUE.get()
            
            if not WORKERS:
                # No workers available, put task back in queue
                TASK_QUEUE.put_nowait(task)
                await asyncio.sleep(1)
                continue
                
            # Get the first available worker (simple round-robin)
            reader, writer = next(iter(WORKERS))
            msg = encode_message(COMMAND_TASK, json.dumps(task).encode())
            writer.write(msg)
            await writer.drain()
            logger.info(f"Assigned task {task['id']} to worker")
            
        except Exception as e:
            logger.error(f"Error assigning task: {e}")

async def main() -> None:
    """Start the distributed task scheduler server."""
    server = await asyncio.start_server(handle_worker, '0.0.0.0', 9001)
    logger.info("Scheduler running on port 9001")
    
    async with server:
        await asyncio.gather(server.serve_forever(), assign_tasks())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
