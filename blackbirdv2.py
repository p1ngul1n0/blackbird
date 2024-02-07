import aiohttp
import asyncio
import requests
from dotenv import load_dotenv
import hashlib
import os
import json

load_dotenv()
listURL = os.getenv("LIST_URL")
listFileName = os.getenv("LIST_FILENAME")


def doSyncRequest(method, url):
    response = requests.request(method=method, url=url)
    parsedData = None

    try:
        parsedData = response.json()
    except:
        pass
    return response, parsedData


async def doAsyncRequest(method, url, session):
    print("Sending request...")
    response = await session.request(method, url)
    parsedData = await response.json()
    return response, parsedData


def readList():
    f = open(listFileName, encoding="UTF-8")
    data = json.load(f)
    return data


def downloadList():
    response, parsedData = doSyncRequest("GET", listURL)
    with open(listFileName, "w", encoding="UTF-8") as f:
        json.dump(parsedData, f, indent=4, ensure_ascii=False)


def hashJSON(jsonData):
    dumpJson = json.dumps(jsonData, sort_keys=True)
    jsonHash = hashlib.md5(dumpJson.encode("utf-8")).hexdigest()
    return jsonHash


async def fetchResults():
    data = readList()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for site in data["sites"]:
            tasks.append(
                doAsyncRequest(method="GET", url=site["uri_check"], session=session)
            )
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


def verifyUsername():
    data = asyncio.run(fetchResults())
    for item in data:
        print(item)


def checkUpdates():
    if os.path.isfile(listFileName):
        print("[-] Checking for updates...")
        data = readList()
        currentListHash = hashJSON(data)
        response, data = doSyncRequest("GET", listURL)
        remoteListHash = hashJSON(data)
        if currentListHash != remoteListHash:
            print("[!] Updating...")
            downloadList()
        else:
            print("[+] List is up to date")
    else:
        print("[!] Downloading WhatsMyName list")
        downloadList()


if __name__ == "__main__":
    checkUpdates()
    verifyUsername()
