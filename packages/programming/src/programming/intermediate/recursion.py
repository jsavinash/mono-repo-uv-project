def countdown(n: int) -> None:
    if n <= 0:
        print(0)
    else:
        print(n)
        countdown(n - 1)


countdown(10)
