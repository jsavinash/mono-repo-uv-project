class ControlStatement:
    def decision_making(self) -> None:
        """Function that demonstrate dicision making in programming"""
        print("*************** Decision Making ***************")
        age = 18
        if age >= 18:
            print("Eligible")
        else:
            print("Not Eligible")

    def fixed_loop(self) -> None:
        """Function that demonstrate fixed loop in programming"""
        print("*************** Fixed Loop ***************")
        for i in range(5):
            print(i)

    def while_loop(self) -> None:
        """Function that demonstrate while loop in programming"""
        print("*************** While Loop ***************")
        num = 0
        while num < 5:
            print(num)
            num += 1

    def switch_case(self) -> None:
        """Function that demonstrate swtich case in programming"""
        print("*************** Switch Case ***************")
        x = "A"
        match x:
            case "A":
                print("A")
            case _:
                print("Default")


cs = ControlStatement()
cs.decision_making()
cs.fixed_loop()
cs.while_loop()
