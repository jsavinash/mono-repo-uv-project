import math


class MathOperation:
    def min(self, a: int, b: int) -> int:
        return min(a, b)

    def max(self, a: int, b: int) -> int:
        return max(a, b)

    def abs(self, a: float) -> float:
        return abs(a)

    def pow(self, x: int, y: int) -> int:
        x = pow(x, y)
        return x

    def sqrt(self, num: int) -> float:
        x = math.sqrt(num)
        return x

    def floor(self, num: float) -> int:
        x = math.floor(num)
        return x

    def ceil(self, num: float) -> int:
        x = math.ceil(num)
        return x


math_operation = MathOperation()
print(math_operation.min(2, 3))
print(math_operation.max(2, 3))
print(math_operation.abs(-7.25))
print(math_operation.pow(4, 3))
print(math_operation.sqrt(64))
print(math_operation.floor(7.5))
print(math_operation.ceil(7.5))
print(math.pi)
