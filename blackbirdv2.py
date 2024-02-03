import aiohttp
import asyncio
import requests
from dotenv import load_dotenv
import hashlib
import os
import json

load_dotenv()
listURL = os.getenv("LIST_URL")


def doSyncRequest(method, url):
    response = requests.request(method=method, url=url)
    parsedData = None

    try:
        parsedData = response.json()
    except:
        pass
    return response, parsedData


def updateList():
    response, parsedData = doSyncRequest("GET", listURL)
    with open("wmn-data.json", "w", encoding="utf-8") as f:
        json.dump(parsedData, f, indent=4)


def checkUpdates():
    if os.path.isfile("wmn-data.json"):
        print("Checking for updates...")
        f = open("wmn-data.json")
        data = json.load(f)
        hashMd5 = hashlib.md5(data.encode("utf-8")).hexdigest()
        print(hashMd5)
    else:
        print("Downloading WhatsMyName list")
        updateList()


if __name__ == "__main__":
    checkUpdates()
