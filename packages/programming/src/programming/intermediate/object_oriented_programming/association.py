"""
One-to-One
One to Many
Many to One
Many-to-Many
"""


# Unidirectional
# (Car knows Driver)
class Driver:
    def __init__(self, name):
        self.name = name


class Car:
    def __init__(self, driver: Driver):
        self.driver = driver


# Bidirectional
# (Both know each other)
class Dog:
    owner: str = ""


class Person:
    def set_dog(self, dog: Dog):
        self.dog = dog
        dog.owner = self
