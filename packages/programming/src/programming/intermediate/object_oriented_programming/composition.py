# Implementation
# (Internal Instantiation)
class Engine:
    def start(self):
        pass


class Car:
    def __init__(self):
        self.engine = Engine()


# Lifecycle Rule
# Engine reference count hits zero when Car is deleted.
