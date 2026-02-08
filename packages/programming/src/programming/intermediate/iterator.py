class MyNumbers:
    def __iter__(self) -> MyNumbers:  # Initializing
        self.a = 1
        return self

    def __next__(self) -> int:  # Operations
        if self.a <= 2:
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration


try:
    my_numbers = MyNumbers()
    my_numbers_itr = iter(my_numbers)
    print(next(my_numbers_itr))
    print(next(my_numbers_itr))
    print(next(my_numbers_itr))
except Exception as error:
    print("Exception", error)
else:
    print("No Error")
finally:
    print("Rest of code executed")
