import asyncio
import time
from typing import List

async def say_after(delay: int, what: str) -> None:
    """
    An asynchronous coroutine that waits for a specified delay and prints a message.

    Args:
        delay: The number of seconds to wait.
        what: The message to print after the delay.
    """
    await asyncio.sleep(delay)
    print(what)

async def main() -> None:
    """
    The main entry point for the asynchronous program.
    """
    start_time: float = time.strftime('%X')
    print(f"Started at {start_time}")

    # Create tasks to run say_after concurrently
    task1: asyncio.Task[None] = asyncio.create_task(say_after(1, 'hello'))
    task2: asyncio.Task[None] = asyncio.create_task(say_after(2, 'world'))

    # Wait until both tasks are completed
    await task1
    await task2

    end_time: float = time.strftime('%X')
    print(f"Finished at {end_time}")

if __name__ == "__main__":
    # Run the main asynchronous function
    asyncio.run(main())
