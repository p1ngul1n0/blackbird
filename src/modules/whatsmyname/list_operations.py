import os
import sys
import config
import json
from rich.console import Console

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from utils.http_client import do_sync_request
from utils.hash import hashJSON

listURL = config.LIST_URL
listPath = config.LIST_PATH

console = Console()

# Read list file and return content
def readList():
    with open(listPath, "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data

# Download .JSON file list from defined URL
def downloadList():
    response, parsedData = do_sync_request("GET", listURL)
    with open(listPath, "w", encoding="UTF-8") as f:
        json.dump(parsedData, f, indent=4, ensure_ascii=False)

# Check for changes in remote list
def checkUpdates():
    if os.path.isfile(listPath):
        console.print(":counterclockwise_arrows_button: Checking for updates...")
        try:
            data = readList()
            currentListHash = hashJSON(data)
            response, data = do_sync_request("GET", listURL)
            remoteListHash = hashJSON(data)
            if currentListHash != remoteListHash:
                console.print(":counterclockwise_arrows_button: Updating...")
                downloadList()
            else:
                console.print("✔️  Sites List is up to date")
        except Exception as e:
            console.print(":police_car_light: Coudn't read local list")
            console.print(":down_arrow: Downloading site list")
            downloadList()
    else:
        console.print(":globe_with_meridians: Downloading site list")
        downloadList()