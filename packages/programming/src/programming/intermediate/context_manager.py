from typing import Optional, Type
from types import TracebackType
from contextlib import contextmanager
from typing import Iterator

#1. Class-Based Context Manager (with Type Hints) 
class MyTimer:
    """A context manager to measure the execution time of a code block."""

    def __init__(self) -> None:
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def __enter__(self) -> "MyTimer":
        """Called when execution enters the context."""
        import time

        self.start_time = time.perf_counter()
        return self  # Returns the context manager instance itself

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Called when execution leaves the context, handles cleanup."""
        import time

        self.end_time = time.perf_counter()
        elapsed_time = (
            self.end_time - self.start_time if self.start_time and self.end_time else 0
        )
        print(f"Elapsed time: {elapsed_time:.4f} seconds")

        # Return True to suppress an exception within the 'with' block, False or None otherwise.
        return None


# Usage
with MyTimer() as timer:
    print("Inside the 'with' block...")
    # Simulate some work
    for _ in range(1000000000):
        pass

#2. Generator-Based Context Manager (with Type Hints)
from contextlib import contextmanager
from typing import Iterator

@contextmanager
def simple_timer(label: str) -> Iterator[None]:
    import time
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"{label}: {end - start:.4f}s")

with simple_timer("Task A"):
    # Simulated work
    sum(range(1_000_000_000))
