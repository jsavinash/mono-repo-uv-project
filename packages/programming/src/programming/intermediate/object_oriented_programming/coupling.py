class MySQL:
    pass


# Tight Coupling
class App:
    def __init__(self):
        self.db = MySQL()  # Hard dependency


# Loose Coupling
class App:
    def __init__(self, database):
        self.db = database  # Injected
