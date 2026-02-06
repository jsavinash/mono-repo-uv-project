from abc import ABC, abstractmethod
from typing import override


class IControlStatement(ABC):
    @abstractmethod
    def decision_making(self) -> None:
        pass

    @abstractmethod
    def fixed_loop(self) -> None:
        pass

    @abstractmethod
    def while_loop(self) -> None:
        pass

    @abstractmethod
    def switch_case(self) -> None:
        pass

    @abstractmethod
    def break_continue(self) -> None:
        pass


class ControlStatement(IControlStatement):
    @override
    def decision_making(self) -> None:
        """Function that demonstrate dicision making in programming"""
        print("*************** Decision Making ***************")
        age = 18
        if age >= 18:
            print("Eligible")
        else:
            print("Not Eligible")

    @override
    def fixed_loop(self) -> None:
        """Function that demonstrate fixed loop in programming"""
        print("*************** Fixed Loop ***************")
        for i in range(5):
            print(i)

    @override
    def while_loop(self) -> None:
        """Function that demonstrate while loop in programming"""
        print("*************** While Loop ***************")
        num = 0
        while num < 5:
            print(num)
            num += 1

    @override
    def switch_case(self) -> None:
        """Function that demonstrate swtich case in programming"""
        print("*************** Switch Case ***************")
        x = "A"
        match x:
            case "A":
                print("A")
            case _:
                print("Default")

    @override
    def break_continue(self) -> None:
        """Function that demonstrate break and continue in programming"""
        print("*************** Break and continue in fixed loop ***************")
        for i in range(5):
            if i == 2:
                print("2 skipped")
                continue
            if i == 4:
                print("4 breaked")
                break
            print(i)


cs = ControlStatement()
cs.decision_making()
cs.fixed_loop()
cs.while_loop()
cs.switch_case()
cs.break_continue()
