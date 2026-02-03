from abc import ABC, abstractmethod


class IndexOutOfBoundsError(IndexError):
    """Exception raised for custom index out of bounds errors. """
    def __init__(self, index, length, message="Index out of bounds"):
        self.index = index
        self.length = length
        self.message = (
            f"{message}: Index {index} is out of bounds for sequence of length {length}"
        )
        super().__init__(self.message)  # Pass the message to the base class constructor

    def __str__(self):
        return self.message


class IFixedArray(ABC):
    """Dynamic array iterface"""

    def __init__(self, capacity: int) -> None:
        self._capacity = capacity

    @property
    def capacity(self):
        return

    @capacity.setter
    def capacity(self, val):
        pass

    @property
    def size(self):
        return

    @size.setter
    def size(self, val):
        pass

    @property
    def arr(self):
        return

    @arr.setter
    def arr(self, val):
        pass

    @abstractmethod  # Decorator to define an abstract method
    def traverse(self):
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
    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._size = 0
        self._arr = [None] * capacity

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, val):
        self._capacity = val

    @property
    def arr(self):
        return self._arr

    @arr.setter
    def arr(self, val):
        self._arr = val

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        self._size = val

    def traverse(self) -> None:
        print(self.arr)

    def insert_at_beginning(self, data: int) -> None:
        curr = data
        for x in range(self.size):
            temp = self.arr[x]
            self.arr[x] = curr
            curr = temp
        self.size += 1

    def insert_at_end(self, data: int) -> None:
        self.arr[self.size] = data
        self.size += 1
        
fixedArray = FixedArray(5)
fixedArray.insert_at_end("One")
fixedArray.insert_at_end("Two")
fixedArray.insert_at_end("Three")
fixedArray.insert_at_end("Four")
fixedArray.insert_at_beginning("Five")
fixedArray.traverse()