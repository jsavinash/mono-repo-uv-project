import json


def json_loader() -> None:
    x = '{ "name":"John", "age":30, "city":"New York"}'
    y = json.loads(x)
    z = json.dumps(y)
    print(y)
    print(z)


json_loader()

y = {
    "name": "John",
    "age": 30,
    "married": True,
    "divorced": False,
    "children": ("Ann", "Billy"),
    "pets": None,
    "cars": [{"model": "BMW 230", "mpg": 27.5}, {"model": "Ford Edge", "mpg": 24.1}],
}

string = json.dumps((y), indent=4, separators=("@", "#"))
print(string)
