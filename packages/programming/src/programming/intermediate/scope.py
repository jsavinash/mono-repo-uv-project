x = "global"

def outer()-> None: #LEGB
    x = "enclosing"
    def inner() -> None:
        x = "local"
        print("Inner", x)
    inner()
    print("Outer", x)

outer()
print("Global", x)
