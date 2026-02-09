import logging
import threading
from time import sleep, perf_counter
from typing import Dict, Any, List

# Configure logging to show which thread is running
logging.basicConfig(
    format="%(asctime)s [%(threadName)s] %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

def count(stop: int = 10) -> None:
    """A function that counts and simulates work with I/O (sleep)."""
    for i in range(stop):
        # The GIL is released during sleep(), allowing other threads to run
        sleep(0.2)
        logging.info(f"count={i}")

def main() -> None:
    """Main function to set up and run threads."""
    start_time: float = perf_counter()

    # Parameters for threads
    thread_configs: List[Dict[str, Any]] = [
        {"name": "Thread-1", "stop": 5},
        {"name": "Thread-2", "stop": 5},
    ]

    threads: List[threading.Thread] = []

    # Create and start threads
    for config in thread_configs:
        thread = threading.Thread(
            target=count,
            args=(config["stop"],),
            name=config["name"],
        )
        threads.append(thread)
        thread.start()

    # Wait for threads to complete
    for thread in threads:
        thread.join()

    end_time: float = perf_counter()
    logging.info(f"Counting finished in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
