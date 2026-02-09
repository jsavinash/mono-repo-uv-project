import functools
from typing import Callable, TypeVar, ParamSpec

# Define TypeVars for the function's parameters and return type
P = ParamSpec("P")
T = TypeVar("T", bound=str)  # Constrain the return type to be a string


def uppercase_decorator(func: Callable[P, T]) -> Callable[P, str]:
    """
    A decorator that converts the result of the decorated function to uppercase.
    Assumes the decorated function returns a string.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
        # Call the original function and convert its result to uppercase
        result = func(*args, **kwargs)
        if isinstance(result, str):
            return result.upper()
        else:
            # Handle cases where the decorated function might return non-string types at runtime
            raise TypeError(
                f"Function {func.__name__} returned non-string type: {type(result)}"
            )

    return wrapper

@uppercase_decorator
def greet(name: str) -> str:
    """Returns a greeting string."""
    return f"Hello, {name}!"


@uppercase_decorator
def say_hello() -> str:
    """Returns a simple hello."""
    return "hello, world!"

# Example usage
print(greet("Alice"))
print(say_hello())
