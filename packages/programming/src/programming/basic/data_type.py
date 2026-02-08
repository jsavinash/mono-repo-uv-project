from abc import ABC
from typing import override
from random import randrange


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
        print(" ********************* String *********************")
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
        print(" ********************* Number *********************")
        print("int value ::", 4)
        print("int type ::", type(4))
        """
        Int
        x = 1
        y = 35656222554887711
        z = -3255522
        """
        print("float value ::", 4.5)
        print("float type ::", type(4.5))
        """ 
        Float
        x = 35e3
        y = 12E4
        z = -87.7e100
        """
        print("complex value ::", 1j)
        print("complex type ::", type(1j))
        """
        Complex
        x = 3+5j
        y = 5j
        z = -5j
        """
        print(" ********************* Conversion *********************")
        print("int (1) => float (1.0)", type(float(1)))
        print("float (1.0) => int (1)", type(int(1.0)))
        print("float (1.0) => complex ((1+0j))", type(complex(1.0)))
        print("complex ((1+0j)) => float Error")
        print("int (1) => complex ((1+0j))", complex(1))
        print("complex ((1+0j)) => int Error")
        print("random numbers", randrange(1, 10))

    @override
    def sequenceTypes(self) -> None:  # 	list, tuple, range
        print(" ********************* Sequence type *********************")
        print(" ********************* List *********************")
        # List items are ordered, changeable, and allow duplicate values.

        #                            0       1         2
        index_based_data_type = ["apple", "banana", "cherry"]
        #                           -3      -2        -1
        print(index_based_data_type)
        print(type(index_based_data_type))

        def access() -> None:
            print(" ********************* Access *********************")
            """
            * [start:end] => we can access data from index start to end - 1.
            * Negative index works in reverse order.
            """
            print(index_based_data_type[0:1])
            print(index_based_data_type[0:])
            print(index_based_data_type[:2])
            print(index_based_data_type[-2:-1])
            print(index_based_data_type[-2:])
            print(index_based_data_type[:-1])
            print("apple" in index_based_data_type)
            print("apple" not in index_based_data_type)

        def change_item() -> None:
            print(" ********************* Change Item *********************")
            print(index_based_data_type)
            index_based_data_type[0] = "mango"
            print(index_based_data_type)
            index_based_data_type[0:2] = ["cheer", "greps"]
            print(index_based_data_type)
            index_based_data_type[2:3] = ["peach", "pomegranate"]
            print(index_based_data_type)
            # Will insert item and shift the current item to next index.
            index_based_data_type.insert(2, "black")
            print(index_based_data_type)

        def add_item() -> None:
            print(" ********************* Add Item *********************")
            item_to_be_extended = ["new_item"]
            item_to_be_extended_tuple = ("new_item_2", "demo_5")
            # Append item without affecting rest of items
            index_based_data_type.append("demo")
            print(index_based_data_type)
            # Insert item at index and shift rest item to next index.
            index_based_data_type.insert(0, "demo2")
            print(index_based_data_type)
            # Extend list
            index_based_data_type.extend(item_to_be_extended)
            print(index_based_data_type)
            # Extend tuple
            index_based_data_type.extend(item_to_be_extended_tuple)
            print(index_based_data_type)

        def remove_item() -> None:
            print(" ********************* Remove Item *********************")
            index_based_data_type.remove("demo_5")  # remove demo_5
            index_based_data_type.pop(0)  # remove first
            index_based_data_type.pop()  # remove last
            print(index_based_data_type)
            del index_based_data_type[0]
            print(index_based_data_type)
            # del index_based_data_type #delete list

        def loop() -> None:
            print(" ********************* Loop *********************")
            for x in index_based_data_type:
                print(x)

        def comprehension() -> None:
            print("********************* Comprehension *********************")
            fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
            new_list = []
            for x in fruits:
                if "a" in x:
                    new_list.append(x)
            print(new_list)
            # [expression for item in iterable if condition == True]
            new_list_2 = [x for x in fruits if "a" in x]
            print(new_list_2)
            new_list_3 = [x.upper() for x in fruits]
            print(new_list_3)
            newlist = [x if x != "banana" else "orange" for x in fruits]
            print(newlist)

        def sort() -> None:
            print("********************* Sort *********************")
            fruits = ["mango", "apple", "banana", "cherry", "kiwi"]
            fruits.sort()
            print(fruits)
            fruits.sort(reverse=True)
            print(fruits)

            def myfunc(n: int) -> int:
                return abs(n - 50)

            thislist = [100, 50, 65, 82, 23]
            thislist.sort(key=myfunc)
            print(thislist)
            fruits.sort(key=str.lower)
            print(fruits)
            fruits.reverse()
            print(fruits)

        def copy() -> None:
            print("********************* Copy *********************")
            alpha_list = ["a", "b", "c", "d"]
            print(alpha_list.copy())
            print(list(alpha_list))
            print(alpha_list[:])

        def join_list() -> None:
            print("********************* Join List *********************")
            list_items = ["a", "b", "c"]
            list_items_2 = ["d", "e", "f"]
            print(list_items + list_items_2)

            # for x in list_items_2:
            #     list_items.append(x)
            # print(list_items)

            list_items_2.extend(list_items)
            print(list_items_2)

        def methods() -> None:
            print("********************* Method List *********************")
            list_items = ["a", "b", "c", "a"]
            print(list_items.count("a"))
            list_items.clear()
            print(list_items)

        access()
        change_item()
        add_item()
        remove_item()
        loop()
        comprehension()
        sort()
        copy()
        join_list()
        methods()
        print(" ********************* Tuple *********************")
        # A tuple is a collection which is ordered and unchangeable.
        tuple_data = ("a", "b", "c")
        print(tuple_data)
        print(type(tuple_data))

        def access_tuple() -> None:
            print(" ********************* Access Tuple *********************")
            print(tuple_data[0])  # Positive index
            print(tuple_data[-1])  # Negative index
            print(
                tuple_data[0:2]
            )  # Range start : end, it will start from start to end - 1.
            print(tuple_data[0:])  # 0 to tupleLength - 1
            print(tuple_data[:2])  # 0 to 1 (2 - 1)
            print(
                tuple_data[-3:-1]
            )  # Range start : end, it will start from start to end - 1.
            print(tuple_data[-3:])  # 0 to tupleLength - 1
            print(tuple_data[:-1])  # 0 to 1 (2 - 1)
            print("a" in tuple_data)
            print("a" not in tuple_data)

        def change_item_tuple() -> None:
            print(" ********************* Change item tuple *********************")
            tuple_data_2 = ("a", "b", "c")
            list_data = list(tuple_data_2)
            list_data[1] = "d"
            tuple_data_3 = tuple(list_data)
            print(tuple_data_3)

        def add_item_tuple() -> None:
            print(" ********************* Add item tuple *********************")
            thistuple = ("apple", "banana", "cherry")
            y = ("orange",)
            demo = thistuple + y
            print(demo)

        def unpacking_tuple() -> None:
            print(" ********************* Unpacking tuple *********************")
            # unpacking with * will give rest of the value in list
            (a, b, *red, c) = ("apple", "banana", "cherry", "pinapple", "grape")
            print(a)  # str
            print(b)  # str
            print(red)  # list
            print(c)  # str

        def loop_tuple() -> None:
            print(" ********************* Loop tuple *********************")
            thistuple = ("apple", "banana", "cherry")
            for x in thistuple:
                print(x)
            for i in range(len(thistuple)):
                print(thistuple[i])
                j = 0
            while j < len(thistuple):
                print(thistuple[j])
                j += 1

        def join_loop_tuple() -> None:
            print(" ********************* Join Loop tuple *********************")
            thistuple = ["a", "b"]
            thistuple_2 = ["c", "d"]
            print(thistuple + thistuple_2)  # contcatenation
            print(thistuple * 2)  # multiply

        def method_tuple() -> None:
            print(" ********************* Method Loop tuple *********************")
            thistuple_2 = ["c", "d", "c", "d"]
            print(thistuple_2.count("d"))
            print(thistuple_2.index("d"))

        def range_method() -> None:
            print(" ********************* Range Method tuple *********************")
            for k in range(0, 10, 2):
                print(k)

        access_tuple()
        change_item_tuple()
        add_item_tuple()
        unpacking_tuple()
        loop_tuple()
        join_loop_tuple()
        method_tuple()
        range_method()

    @override
    def mappingType(self) -> None:  # 	dict
        print(" ********************* Dict *********************")
        """
        Dictionaries are used to store data values in key:value pairs.
        A dictionary is a collection which is ordered*, changeable and do not allow duplicates.
        """
        thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}
        print(thisdict)
        print(len(thisdict))
        print(type(thisdict))
        # The dict() Constructor
        print(dict(name="Avinash"))

        def access_dict() -> None:
            print(" ********************* Access Dict *********************")
            thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}
            print(thisdict["brand"])  # via referring key
            print(thisdict.get("model"))  # get method
            keys = thisdict.keys()
            values = thisdict.values()
            items = thisdict.items()
            print(keys)  # Return list with keys
            print(values)  # Return list with values
            print(items)  # Return list of dict.
            for item in items:
                print(f"{item[0]} :: {item[1]}")
            print("brand" in thisdict)
            print("brand" not in thisdict)

        def change_dict() -> None:
            print(" ********************* Change Dict *********************")
            thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}
            print(thisdict)
            thisdict["brand"] = "Tata"
            print(thisdict)
            thisdict.update({"year": 2020})
            print(thisdict)

        def add_dict() -> None:
            print(" ********************* Add Dict *********************")
            thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}
            print(thisdict)
            thisdict["wheels"] = 4
            print(thisdict)
            thisdict.update({"color": "red"})
            print(thisdict)

        def remove_dict() -> None:
            print(" ********************* Remove Dict *********************")
            thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}
            del thisdict["year"]
            print(thisdict)
            thisdict.pop("model")
            print(thisdict)
            thisdict.popitem()
            print(thisdict)
            # del thisdict

        def loop_dict() -> None:
            print(" ********************* Loop Dict *********************")
            thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}
            keys = thisdict.keys()
            values = thisdict.values()
            items = thisdict.items()
            for i in keys:
                print(i)
            for j in values:
                print(j)
            for k, l in items:
                print(f"{k} :: {l}")

        def copy_dict() -> None:
            print(" ********************* Copy Dict *********************")
            thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}
            print(thisdict.copy())
            print(dict(thisdict))

        access_dict()
        change_dict()
        add_dict()
        remove_dict()
        loop_dict()
        copy_dict()

    @override
    def setType(self) -> None:  # 	set, frozenset
        print(" ********************* Set *********************")
        # A set is a collection which is unordered, unchangeable*, and unindexed.
        myset = {"apple", "banana", "cherry"}
        print(myset)
        print(type(myset))
        print(len(myset))

        def access_or_loop_set() -> None:
            print(" ********************* Access or Loop Set *********************")
            for x in myset:
                print(x)
            print("apple" in myset)
            print("apple" not in myset)

        def change_set() -> None:
            print(" ********************* Change Set *********************")
            print("Once it's created, we can't changed it")

        def add_item() -> None:
            print(" ********************* Add Set *********************")
            myset.add("pinapple")
            print(myset)
            add_newset = {"coconut"}  # set
            add_newset_2 = ["jackfruit"]  # list
            myset.update(add_newset, add_newset_2)
            print(myset)

        def remove_item() -> None:
            print(" ********************* Remove Set *********************")
            myset.remove("banana")  # will raise error if not exist
            myset.discard("banana")  # will not raise error if not exist
            myset.pop()  # will remove random items
            myset.clear()
            # del myset
            print(myset)

        def join_item() -> None:
            print(" ********************* Join Set *********************")
            set1 = {"a", "b", "c"}
            set2 = {1, 2, 3}
            # print(set3.update(set2)) #Add element from set2 to set1
            print("union ::", set1.union(set2))  # union
            print(" | ::", set1 | set2)  # union
            print("intersection ::", set1.intersection(set2))  # intersection
            print(" & ::", set1 & set2)  # intersection
            set3 = {"a", "b", "c"}
            set4 = {"c", "d", "e"}
            print(
                "difference ::", set3.difference(set4)
            )  # difference find item from set3 which is there in set4 and remove it.
            print(
                " - ::", set3 - set4
            )  # difference find item from set3 which is there in set4 and remove it.
            # print("difference ::", set3.difference_update(set4)) #difference find item from set3 which is there in set4 and remove it.
            print(
                "symmetric difference ::", set3.symmetric_difference(set4)
            )  # difference find item from set3 which is there in set4 and remove it.
            print(
                " ^ ::", set3 ^ set4
            )  # difference find item from set3 which is there in set4 and remove it.

        def forzeset() -> None:
            print(" ********************* forzeset *********************")
            x = frozenset({"apple", "banana", "cherry"})
            print(x)
            print(type(x))


        access_or_loop_set()
        change_set()
        add_item()
        remove_item()
        join_item()
        forzeset()

    @override
    def booleanType(self) -> None:  # 	bool
        print(" ********************* Boolean *********************")
        print("Value ::", True)
        print("Type", type(True))
        print(bool("Hello"))
        print(bool(15))
        print(bool())

    @override
    def binaryTypes(self) -> None:  # 	bytes, bytearray, memoryview
        print("Demo")

    @override
    def noneType(self) -> None:  # 	NoneType
        print(" ********************* None *********************")
        print(None)
        print(type(None))


dataType = DataType()
# dataType.textType()
# dataType.booleanType()
# dataType.noneType()
# dataType.numericTypes()
# dataType.sequenceTypes()
# dataType.mappingType()
dataType.setType()
