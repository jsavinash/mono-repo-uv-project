from abc import ABC, abstractmethod
from typing import override


class IndexOutOfBoundsError(IndexError):
    """Exception raised for custom index out of bounds errors."""

    @override
    def __init__(
        self, index: int, length: int, message: str = "Index out of bounds"
    ) -> None:
        self.index = index
        self.length = length
        self.message = (
            f"{message}: Index {index} is out of bounds for sequence of length {length}"
        )
        super().__init__(self.message)  # Pass the message to the base class constructor

    @override
    def __str__(self) -> str:
        return self.message


class IFixedArray(ABC):
    """Dynamic array iterface"""

    def __init__(self, capacity: int) -> None:
        self._capacity = capacity

    @property
    @abstractmethod
    def capacity(self) -> int:
        pass

    @capacity.setter
    @abstractmethod
    def capacity(self, val: int) -> None:
        pass

    @property
    @abstractmethod
    def size(self) -> int:
        pass

    @size.setter
    @abstractmethod
    def size(self, val: int) -> None:
        pass

    @property
    @abstractmethod
    def arr(self) -> list[str | None]:
        pass

    @arr.setter
    @abstractmethod
    def arr(self, val: list[str | None]) -> None:
        pass

    @abstractmethod  # Decorator to define an abstract method
    def traverse(self) -> None:
        pass

    def insert_at_beginning(self, data: str) -> None:
        pass

    def insert_at_idx(self, data: str, idx: int) -> None:
        pass

    def insert_at_end(self, data: str) -> None:
        pass

    def deleteAtBeginning(self) -> None:
        pass

    def deleteAtIdx(self, idx: int) -> None:
        pass

    def deleteAtEnd(self) -> None:
        pass

    def deleteFirstOccurrence(self, data: str) -> None:
        pass

    def deleteAllOccurrence(self, data: str) -> None:
        pass


class FixedArray(IFixedArray):
    capacity: int = 0
    size: int = 0
    arr: list[str | None] = []

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.size = 0
        self.arr = [None] * capacity

    @override
    def traverse(self) -> None:
        print(self.arr)

    @override
    def insert_at_beginning(self, data: str | None) -> None:
        try:
            curr = data
            for x in range(self.size):
                temp = self.arr[x]
                self.arr[x] = curr
                curr = temp
            self.size += 1
        except Exception as error:
            print("An exception occurred:", error)

    @override
    def insert_at_end(self, data: str) -> None:
        try:
            self.arr[self.size] = data
            self.size += 1
        except Exception as error:
            print("An exception occurred:", error)


fixedArray = FixedArray(5)
fixedArray.insert_at_end("One")
fixedArray.insert_at_end("Two")
fixedArray.insert_at_end("Three")
fixedArray.insert_at_end("Four")
fixedArray.insert_at_beginning("Five")
fixedArray.traverse()
