"""
* Encapsulation means hiding internal details of a class
* and only exposing what’s necessary via access modifier.
* Public members are variables or methods that can be accessed from anywhere inside the class, outside the class or from other modules
* Protected members are variables or methods that are intended to be accessed only within the class and its subclasses.
* Private members are variables or methods that cannot be accessed directly from outside the class. 
"""


class Encapsulation:
    def __init__(self, name: str, salary: int) -> None:
        self.name = name  # public attribute
        self.__salary = salary  # private attribute


encapsulation = Encapsulation("Avinash", 23000)
try:
    print(encapsulation.name)
    print(encapsulation.__salary)
except:
    print("Error")
