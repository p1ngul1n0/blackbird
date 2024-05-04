import re
import config
import sys

def filterFoundAccounts(site):
    if site["status"] == "FOUND":
        return True
    else:
        return False

def filterAccounts(filter, site):
    match = re.match(r'^([^=]+)=(.+)', filter)
    
    if (match):
        prop = match.group(1)
        value = match.group(2)
        if (str(site[prop]) == value):
            return True
        else:
            return False
    else:
        config.console.print("⭕ Filter is not in correct format")
        sys.exit()