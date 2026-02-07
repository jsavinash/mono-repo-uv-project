from abc import ABC
from typing import override


# Built-in Data Types
class IDataType(ABC):
    def textType(self) -> None: ...  # str

    def numericTypes(self) -> None: ...  # 	int, float, complex

    def sequenceTypes(self) -> None: ...  # 	list, tuple, range

    def mappingType(self) -> None: ...  # 	dict

    def setType(self) -> None: ...  # 	set, frozenset

    def booleanType(self) -> None: ...  # 	bool

    def binaryTypes(self) -> None: ...  # 	bytes, bytearray, memoryview

    def noneType(self) -> None: ...  # 	NoneType


class DataType(IDataType):
    @override
    def textType(self) -> None:  # str
        value: str = "String value"
        print("Str :: ", value)
        print("Type :: ", type(value))
        print("Type Casting :: ", str(2))

        def slicing() -> None:
            print(" ********************* String Slicing *********************")
            print("value[start:end] :: (start) to (end - 1)")
            value: str = "Hello, World!"
            print("value[2:5] :: (2) to (5 - 1) :: ", value[2:5])
            print("value[2:] :: (2) to end :: ", value[2:])
            print("value[:5] :: (0) to (5-1) :: ", value[:5])

        def modify() -> None:
            print(" ********************* String Modify *********************")
            value: str = "Hello, World!"
            print("Upper :: ", value.upper())
            print("Lower :: ", value.lower())
            print("Strip :: ", value.strip())
            print("Replace :: ", value.replace("H", "A"))
            print("Split :: ", value.split(","))

        def concatenation() -> None:
            print(" ********************* String Concatenation *********************")
            value: str = "Hello, World!"
            value2: str = "Hello, World!"
            print("(+) concatenation :: ", value + " " + value2)

        def format_strings() -> None:
            print(" ********************* Format - Strings *********************")
            value: int = 20
            print(f"My age is {value:.2f}")

        def escape_character() -> None:
            print(" ********************* Escape Character *********************")
            # txt: str = "We are the so-called "Vikings" from the north."
            txt: str = 'We are the so-called "Vikings" from the north.'
            print(txt)

        def string_method() -> None:
            value: str = "hello, World!"
            print("Index :: ", value.index("World"))
            print("Capitalize (first letter) :: ", value.capitalize())
            print("Is alphabet string :: ", "Hello".isalpha())
            print("String format :: ")
            txt1 = "My name is {fname}, I'm {age}".format(fname="John", age=36)
            txt2 = "My name is {0}, I'm {1}".format("John", 36)
            txt3 = "My name is {}, I'm {}".format("John", 36)
            print(txt1)
            print(txt2)
            print(txt3)
            print("String join :: ")
            myTuple = ("John", "Peter", "Vicky")
            x = "#".join(myTuple)
            print(x)
            myDict = {"name": "John", "country": "Norway"}
            mySeparator = "TEST"
            x = mySeparator.join(myDict)
            print(x)

        slicing()
        modify()
        concatenation()
        format_strings()
        escape_character()
        string_method()

    @override
    def numericTypes(self) -> None:  # 	int, float, complex
        print("Demo")

    @override
    def sequenceTypes(self) -> None:  # 	list, tuple, range
        print("Demo")

    @override
    def mappingType(self) -> None:  # 	dict
        print("Demo")

    @override
    def setType(self) -> None:  # 	set, frozenset
        print("Demo")

    @override
    def booleanType(self) -> None:  # 	bool
        print("Demo")

    @override
    def binaryTypes(self) -> None:  # 	bytes, bytearray, memoryview
        print("Demo")

    @override
    def noneType(self) -> None:  # 	NoneType
        print("Demo")


dataType = DataType()
dataType.textType()
