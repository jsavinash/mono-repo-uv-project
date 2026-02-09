from typing import Callable, TypedDict, Unpack

def add(a: int, b: int) -> int:
    return a + b


x: Callable[[int, int], int] = lambda a, b: a + b


def add_positional_only(a: int, /) -> int:
    return a + 1


def add_without_positional_only(a: int) -> int:
    return a + 1


def add_keyword_only(*, a: int) -> int:
    return a + 1


def add_without_keyword_only(a: int) -> int:
    return a + 1


def my_function(a: int, b: int, /, *, c: int, d: int) -> int:
    return a + b + c + d


# Arbitrary Arguments - *args
def arbitrary_arguments_func(*args: str) -> str:
    return args[0] + args[1] + args[2]

class Options(TypedDict):
    lname: str

#Arbitrary Keyword Arguments - **kwargs
def arbitrary_keyword_arguments_func(**kwargs: Unpack[Options]) -> None:
  print("His last name is " + kwargs["lname"])

print(add(1, 2))
print(x(1, 2))
print(add_without_positional_only(a=1))
print(add_positional_only(1))
print(add_keyword_only(a=1))
print(add_without_keyword_only(1))
print(my_function(1, 2, c=3, d=4))
print(arbitrary_arguments_func("a", "b", "c"))
arbitrary_keyword_arguments_func(lname = "Nishad")
