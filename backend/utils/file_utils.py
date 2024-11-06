import os

def check_file_exists(filename):
    return os.path.exists(filename)

def read_file(filename):
    with open(filename, "r") as file:
        return file.read()
