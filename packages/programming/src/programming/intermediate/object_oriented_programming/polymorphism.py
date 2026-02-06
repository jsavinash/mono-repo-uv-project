from abc import ABC, abstractmethod
from typing import override, overload

"""
* If one task is performed in different ways, it is known as polymorphism. 
* Overriding supported.
* Overloading is not supported.
"""


class IAnimal(ABC):
    @abstractmethod
    def sound(self) -> None: ...

    # @abstractmethod
    # def area(self) -> int: ...

class Animal(IAnimal):
    @override
    def sound(self) -> None:
        print("An animal makes a sound")

    # @overload
    # def area(self, width: int, height: int) -> int: ...
    
    # @overload
    # def area(self, side: int) -> int: ...

    # # Implementation
    # def area(self, *args) -> int:
    #     if len(args) == 2:
    #         return args[0] * args[1]
    #     elif len(args) == 1:
    #         return args[0] ** 2
    #     return 0


class Dog(Animal):
    @override
    def sound(self) -> None:
        print("Dog barks")


class Cat(Animal):
    @override
    def sound(self) -> None:
        print("Cat barks")


animal = Animal()
# print(animal.area(5, 10)) # Output: 50
# print(animal.area(5)) 
dog = Dog()
cat = Cat()
print("Animal Executed ::")
animal.sound()
print("Dog Executed ::")
dog.sound()
print("Cat Executed ::")
cat.sound()
