import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', ''))

from utils.log import logError

# Dump HTML data to a .html file
def dumpHTML(path, content):
    try:
        with open(path, "w", encoding="utf-8") as htmlFile:
            htmlFile.write(content)
        return True
    except Exception as e:
        logError(e, f"Coudn't DUMP data to HTML file!")
        return False