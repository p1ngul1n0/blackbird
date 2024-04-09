import aiohttp
import asyncio
import requests
from dotenv import load_dotenv
import hashlib
import os
import json
import argparse
import time
from rich.console import Console
import csv
from datetime import datetime
import logging


console = Console()

load_dotenv()
listURL = os.getenv("LIST_URL")
listFileName = os.getenv("LIST_FILENAME")
proxy = os.getenv("PROXY") if os.getenv("USE_PROXY") == "TRUE" else None
proxies = {"http": proxy, "https": proxy} if os.getenv("USE_PROXY") == "TRUE" else None
logging.basicConfig(
    filename=os.getenv("LOG_FILENAME"),
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
requests.packages.urllib3.disable_warnings()


# Perform a Sync Request and return response details
def do_sync_request(method, url):
    response = requests.request(
        method=method,
        url=url,
        proxies=proxies,
        timeout=args.timeout,
        verify=False,
    )
    parsedData = None
    try:
        parsedData = response.json()
    except Exception as e:
        logError(e, f"Error in Sync HTTP Request [{method}] {url}")
    return response, parsedData


# Perform an Async Request and return response details
async def do_async_request(method, url, session):
    try:
        response = await session.request(
            method,
            url,
            proxy=proxy,
            timeout=args.timeout,
            allow_redirects=True,
            ssl=False,
        )

        content = await response.text()
        responseData = {
            "url": url,
            "status_code": response.status,
            "headers": response.headers,
            "content": content,
        }
        return responseData
    except Exception as e:
        logError(e, f"Error in Async HTTP Request [{method}] {url}")
        return None


# Read list file and return content
def readList():
    with open(listFileName, "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


# Download .JSON file list from defined URL
def downloadList():
    response, parsedData = do_sync_request("GET", listURL)
    with open(listFileName, "w", encoding="UTF-8") as f:
        json.dump(parsedData, f, indent=4, ensure_ascii=False)


# Return MD5 HASH for given JSON
def hashJSON(jsonData):
    dumpJson = json.dumps(jsonData, sort_keys=True)
    jsonHash = hashlib.md5(dumpJson.encode("utf-8")).hexdigest()
    return jsonHash


def logError(e, message):
    if args.verbose:
        console.print(f"⛔  {message}")
        console.print("     | An error occurred:")
        if str(e) != "":
            console.print(f"     | {str(e)}")
            logging.error(f"{message} | {str(e)}")
        else:
            console.print(f"     | {repr(e)}")
            logging.error(f"{message} | {repr(e)}")


# Save results to CSV file
def saveToCsv(results):
    try:
        fileName = results["username"] + "_" + results["date"] + "_blackbird.csv"
        with open(
            fileName,
            "w",
            newline="",
        ) as file:
            writer = csv.writer(file)
            writer.writerow(["name", "url", "status"])
            for result in results["results"]:
                writer.writerow([result["name"], result["url"], result["status"]])
        console.print(f"💾  Saved results to '[cyan1]{fileName}[/cyan1]'")
    except Exception as e:
        logError(e, "Coudn't saved results to CSV file!")


# Verify account existence based on list args
async def checkSite(site, method, url, session):
    returnData = {"name": site["name"], "url": url, "status": "NONE"}
    response = await do_async_request(method, url, session)
    if response == None:
        returnData["status"] = "ERROR"
        return returnData
    try:
        if response:
            if (site["e_string"] in response["content"]) and (
                site["e_code"] == response["status_code"]
            ):
                if (site["m_string"] not in response["content"]) and (
                    site["m_code"] != response["status_code"]
                ):
                    returnData["status"] = "FOUND"
                    console.print(
                        f"  ✔️  \[[cyan1]{site['name']}[/cyan1]] [bright_white]{response['url']}[/bright_white]"
                    )
            else:
                returnData["status"] = "NOT-FOUND"
                if args.verbose:
                    console.print(
                        f"  ❌ [[blue]{site['name']}[/blue]] [bright_white]{response['url']}[/bright_white]"
                    )
            return returnData
    except Exception as e:
        logError(e, f"Coudn't check {site['name']} {url}")
        return returnData


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
        tasksResults = await asyncio.gather(*tasks, return_exceptions=True)
        dateNow = datetime.now().strftime("%m-%d-%Y")
        results = {
            "results": tasksResults,
            "username": username,
            "date": dateNow,
        }
    return results


# Start username check and presents results to user
def verifyUsername(username):
    console.print(
        f':play_button: Enumerating accounts with username "[cyan1]{username}[/cyan1]"'
    )
    start_time = time.time()
    results = asyncio.run(fetchResults(username))
    end_time = time.time()
    console.print(
        f":chequered_flag: Check completed in {int(end_time - start_time)} seconds ({len(results['results'])} sites)"
    )
    if args.csv:
        saveToCsv(results)


# Check for changes in remote list
def checkUpdates():
    if os.path.isfile(listFileName):
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
                console.print("✔️  List is up to date")
        except Exception as e:
            console.print(":police_car_light: Coudn't read local list")
            console.print(":down_arrow: Downloading WhatsMyName list")
            downloadList()
    else:
        console.print(":globe_with_meridians: Downloading WhatsMyName list")
        downloadList()


if __name__ == "__main__":
    console.print(
        """[red]
    ▄▄▄▄    ██▓    ▄▄▄       ▄████▄   ██ ▄█▀ ▄▄▄▄    ██▓ ██▀███  ▓█████▄ 
    ▓█████▄ ▓██▒   ▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█████▄ ▓██▒▓██ ▒ ██▒▒██▀ ██▌
    ▒██▒ ▄██▒██░   ▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒██▒ ▄██▒██▒▓██ ░▄█ ▒░██   █▌
    ▒██░█▀  ▒██░   ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ▒██░█▀  ░██░▒██▀▀█▄  ░▓█▄   ▌
    ░▓█  ▀█▓░██████▒▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░▓█  ▀█▓░██░░██▓ ▒██▒░▒████▓ 
    ░▒▓███▀▒░ ▒░▓  ░▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░▒▓███▀▒░▓  ░ ▒▓ ░▒▓░ ▒▒▓  ▒ 
    ▒░▒   ░ ░ ░ ▒  ░ ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░▒░▒   ░  ▒ ░  ░▒ ░ ▒░ ░ ▒  ▒ 
    ░    ░   ░ ░    ░   ▒   ░        ░ ░░ ░  ░    ░  ▒ ░  ░░   ░  ░ ░  ░ 
    ░          ░  ░     ░  ░░ ░      ░  ░    ░       ░     ░        ░    
        ░                  ░                     ░               ░      

    [/red]"""
    )
    console.print(
        "[white]Made with :beating_heart: by Lucas Antoniaci ([red]p1ngul1n0[/red])[/white]"
    )

    parser = argparse.ArgumentParser(
        prog="blackbird",
        description="An OSINT tool to search for accounts by username in social networks.",
    )
    parser.add_argument("-u", "--username", required=True)
    parser.add_argument("--csv", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument(
        "-v", "--verbose", default=False, action=argparse.BooleanOptionalAction
    )
    parser.add_argument("-t", "--timeout", type=int, default=30)

    args = parser.parse_args()

    checkUpdates()

    if args.username:
        verifyUsername(args.username)
