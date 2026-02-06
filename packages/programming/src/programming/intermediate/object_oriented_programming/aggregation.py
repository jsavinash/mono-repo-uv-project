#Class Structure
#(Independent Parts)
# Losely coupled
class Department:
    def __init__(self, name):
        self.name = name

class University:
    def __init__(self, depts):
        self.depts = depts

#Lifecycle Independence
d = Department("CS")
u = University([d])
# If 'u' is deleted, 'd' persists