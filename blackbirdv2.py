import aiohttp
import asyncio
import requests
from dotenv import load_dotenv
import hashlib
import os
import json
import argparse
import time


load_dotenv()
listURL = os.getenv("LIST_URL")
listFileName = os.getenv("LIST_FILENAME")
proxy = os.getenv("PROXY") if os.getenv("USE_PROXY") == "TRUE" else None
requests.packages.urllib3.disable_warnings()


# Perform a Sync Request and return response details
def doSyncRequest(method, url):
    response = requests.request(method=method, url=url, proxies=proxy, verify=False)
    parsedData = None

    try:
        parsedData = response.json()
    except:
        pass
    return response, parsedData


# Perform an Async Request and return response details
async def doAsyncRequest(method, url, session):
    try:
        response = await session.request(method, url, proxy=proxy, ssl=False, timeout=5)

        content = await response.text()
        responseData = {
            "url": url,
            "status_code": str(response.status) + " " + response.reason,
            "headers": response.headers,
            "content": content,
        }
        return responseData
    except Exception as e:
        # print(e)
        return None


# Read list file and return content
def readList():
    with open(listFileName, "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


# Download .JSON file list from defined URL
def downloadList():
    response, parsedData = doSyncRequest("GET", listURL)
    with open(listFileName, "w", encoding="UTF-8") as f:
        json.dump(parsedData, f, indent=4, ensure_ascii=False)


# Return MD5 HASH for given JSON
def hashJSON(jsonData):
    dumpJson = json.dumps(jsonData, sort_keys=True)
    jsonHash = hashlib.md5(dumpJson.encode("utf-8")).hexdigest()
    return jsonHash


# Verify account existence based on list args
async def checkSite(site, method, url, session):
    response = await doAsyncRequest(method, url, session)
    print(f"[+] [{site['name']}] {response['url']} [{response['status_code']}]")
    return {
        "site": site,
        "response": response,
    }


# Control survey on list sites
async def fetchResults(username):
    data = readList()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for site in data["sites"]:
            tasks.append(
                checkSite(
                    site=site,
                    method="GET",
                    url=site["uri_check"].replace("{account}", username),
                    session=session,
                )
            )
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


# Start username check and presents results to user
def verifyUsername(username):
    start_time = time.time()
    results = asyncio.run(fetchResults(username))
    end_time = time.time()
    print(
        f"[!] Check completed in {int(end_time - start_time)} seconds ({len(results)} sites)"
    )


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
    parser = argparse.ArgumentParser(
        prog="Blackbird",
        description="An OSINT tool to search for accounts by username in social networks.",
    )
    parser.add_argument("-u", "--username")
    args = parser.parse_args()
    if args.username:
        verifyUsername(args.username)
