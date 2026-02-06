"""
* When one object acquires all the properties and behaviors of a parent object,
* it is known as inheritance.
* It provides code reusability. It is used to achieve runtime polymorphism.
"""


class Parent:
    classname: str = "Parent"

    def get_parent_classname(self) -> None:
        print(self.classname)


class Child(Parent):
    pass


child = Child()  # Child acquire all properties (state, behavior) of parant
child.get_parent_classname()
