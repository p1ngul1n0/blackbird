import config
import os

# Dump HTML data to a .html file
def dumpHTML(path, content):
    with open(path, "w") as htmlFile:
        htmlFile.write(content)