import multiprocessing
import typing as t
import time
import os

# Define the function that will be executed in a separate process.
# Type hints specify the input and output types.
def cube(num: int) -> int:
    """Function to calculate the cube of a number."""
    # Simulate a time-consuming task
    time.sleep(0.1) 
    result = num * num * num
    print(f"Process ID: {os.getpid()} | Input: {num} | Result: {result}")
    return result

if __name__ == "__main__":
    # This block is essential for multiprocessing on all operating systems.
    # It ensures the child processes only run the target function, not the main script logic.
    
    # The list of numbers to process
    numbers_to_process: t.List[int] = list(range(1, 6))

    # Create a multiprocessing Pool to manage a number of worker processes
    # (defaults to the number of CPUs)
    with multiprocessing.Pool() as pool:
        # Map the 'cube' function to each item in 'numbers_to_process' in parallel.
        # Pool.map handles distributing the data and collecting results automatically.
        # The return type is explicitly hinted.
        results: t.List[int] = pool.map(cube, numbers_to_process)

    print("-" * 20)
    print(f"Main Process ID: {os.getpid()}")
    print(f"All results (ordered): {results}")
    print("Done!")

    