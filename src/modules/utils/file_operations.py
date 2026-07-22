import os


def isFile(fileName):
    return os.path.isfile(fileName)


def getLinesFromFile(fileName):
    try:
        with open(fileName) as f:
            return f.read().splitlines()
    except OSError:
        return []
