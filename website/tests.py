import os

path = "images/"

file = os.path.join(path, "test.jpg")

print(os.getcwd())

os.remove(file)