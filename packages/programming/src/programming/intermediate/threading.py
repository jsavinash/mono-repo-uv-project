import threading
import time
from typing import List, Any

def task(name: str, duration: int) -> None:
    """
    Simulates a task running in a separate thread.

    Args:
        name: The name of the task.
        duration: The time in seconds the task will run.
    """
    print(f"Thread {name}: starting (will run for {duration} seconds)...")
    time.sleep(duration)  # Simulate an I/O operation
    print(f"Thread {name}: finishing.")

def main() -> None:
    """
    Main function to demonstrate threading with type hints.
    """
    # Create the thread object, passing the target function and its arguments
    thread_args: tuple[Any, ...] = ("A", 2)
    my_thread: threading.Thread = threading.Thread(target=task, args=thread_args)
    
    # Start the thread
    my_thread.start()
    
    print("Main thread: doing other work concurrently.")
    
    # Wait for the thread to finish before the main program exits
    my_thread.join()
    
    print("Main thread: all done.")

if __name__ == "__main__":
    main()
