from abc import ABC, abstractmethod

"""
* Data abstraction means showing only the essential features 
* and hiding the complex internal details. Technically, in 
* Python abstraction is used to hide the implementation details 
* from the user and expose only necessary parts, 
* making the code simpler and easier to interact with.
"""


# Abstract :- combination of abstract or shared methods.
class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

    def move(self):
        return "The animal moves."


# Interface :- all methods are abstract
class Flyable(ABC):
    @abstractmethod
    def take_off(self):
        pass

    @abstractmethod
    def land(self):
        pass
