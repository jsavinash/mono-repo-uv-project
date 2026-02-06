from typing import override

"""
* Class is a logical entity.
* A class can also be defined as a blueprint from which we can create an individual object. 
* Class does not consume any space.
"""


class Bank:
    """Constructor function for bank class"""

    def __init__(self, name: str = "No name given"):
        self.name = name  # This calls the setter

    @property
    def name(self) -> str:
        """I'm the 'name' property getter."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """I'm the 'name' property setter with validation."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value

    @override
    def __str__(self) -> str:
        """Returns a user-friendly string representation of the object."""
        return f"Bank named :: {self.name}"


bank = Bank("HDFC Bank")
print(bank)
