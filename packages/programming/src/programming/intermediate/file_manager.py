import os

script_directory = os.path.dirname(os.path.abspath(__file__))
file_directory = f"{script_directory}/file_management"
file_path = f"{script_directory}/file_management/demofile.txt"

os.mkdir(f"{script_directory}/file_management")
with open(file_path, "x") as f:  # create file
    f.write("New file content")

with open(file_path, "w") as f:  # override
    # print(f.read(5)) #Read full file
    # print(f.readline(3)) #One Line
    f.write("Content deleted")

with open(file_path, "a") as f:  # Append
    # print(f.read(5)) #Read full file
    # print(f.readline(3)) #One Line
    f.write("\nHello World!")

with open(file_path) as f:  # Read
    print(f.read())  # Read full file
    # print(f.readline(3)) #One Line
    # for x in f:
    #     print(x) #Line by line with newline

if os.path.exists(file_path):
    os.remove(file_path)
else:
    print("The file does not exist")

os.rmdir(file_directory)
