import os
import sys
import config
import json
from rich.console import Console

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from utils.http_client import do_sync_request
from utils.hash import hashJSON
from utils.log import logError

usernameListURL = config.USERNAME_LIST_URL
usernameListPath = config.USERNAME_LIST_PATH
emailListPath = config.EMAIL_LIST_PATH
usernameMetadataListPath = config.USERNAME_METADATA_LIST_PATH

console = Console()


# Read list file and return content
def readList(option):
    if option == "username":
        with open(usernameListPath, "r", encoding="UTF-8") as f:
            data = json.load(f)
        return data
    elif option == "email":
        with open(emailListPath, "r", encoding="UTF-8") as f:
            data = json.load(f)
        return data
    elif option == "metadata":
        with open(usernameMetadataListPath, "r", encoding="UTF-8") as f:
            data = json.load(f)
        return data
    else:
        return False


# Download .JSON file list from defined URL
def downloadList():
    response = do_sync_request("GET", usernameListURL)
    with open(usernameListPath, "w", encoding="UTF-8") as f:
        json.dump(response.json(), f, indent=4, ensure_ascii=False)


# Check for changes in remote list
def checkUpdates():
    if os.path.isfile(usernameListPath):
        console.print(":counterclockwise_arrows_button: Checking for updates...")
        try:
            data = readList("username")
            currentListHash = hashJSON(data)
            response = do_sync_request("GET", usernameListURL)
            remoteListHash = hashJSON(response.json())
            if currentListHash != remoteListHash:
                console.print(":counterclockwise_arrows_button: Updating...")
                downloadList()
            else:
                console.print("✔️  Sites List is up to date")
        except Exception as e:
            console.print(":police_car_light: Coudn't read local list")
            console.print(":down_arrow: Downloading site list")
            logError(e, f"Coudn't read local list")
            downloadList()
    else:
        console.print(":globe_with_meridians: Downloading site list")
        downloadList()
