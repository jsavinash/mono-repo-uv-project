import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
if x:
    print("Matched")
else:
    print("Not Matched")

