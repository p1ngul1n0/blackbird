import sys
import os
import time
import aiohttp
import asyncio
from modules.whatsmyname.list_operations import readList
from modules.utils.filter import filterFoundAccounts, filterAccounts
from modules.utils.http_client import do_async_request
from modules.utils.log import logError
from modules.export.csv import saveToCsv
from modules.export.pdf import saveToPdf
import config
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

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
                    config.console.print(
                        f"  ✔️  \[[cyan1]{site['name']}[/cyan1]] [bright_white]{response['url']}[/bright_white]"
                    )
            else:
                returnData["status"] = "NOT-FOUND"
                if config.verbose:
                    config.console.print(
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

        if config.filter:
            sitesToSearch = list(filter(lambda x: filterAccounts(config.filter, x), data["sites"]))
            if (len(sitesToSearch)) <= 0:
                config.console.print(f"⭕ No sites found for the given filter {config.filter}")
                sys.exit()
            else:
                config.console.print(f":page_with_curl: {len(sitesToSearch)} sites found for the given filter {config.filter}")
        else:
            sitesToSearch = data["sites"]

        for site in sitesToSearch:
            tasks.append(
                checkSite(
                    site=site,
                    method="GET",
                    url=site["uri_check"].replace("{account}", username),
                    session=session,
                )
            )
        tasksResults = await asyncio.gather(*tasks, return_exceptions=True)
        dateRaw = datetime.now().strftime("%m_%d_%Y")
        datePretty = datetime.now().strftime("%B %d, %Y")
        results = {
            "results": tasksResults,
            "username": username,
            "date": dateRaw,
            "pretty-date": datePretty
        }
    return results


# Start username check and presents results to user
def verifyUsername(username):
    config.console.print(
        f':play_button: Enumerating accounts with username "[cyan1]{username}[/cyan1]"'
    )
    start_time = time.time()
    results = asyncio.run(fetchResults(username))
    end_time = time.time()
    config.console.print(
        f":chequered_flag: Check completed in {round(end_time - start_time, 1)} seconds ({len(results['results'])} sites)"
    )
    foundAccounts = list(filter(filterFoundAccounts, results["results"]))
    if (len(foundAccounts) > 0):
        if config.csv:
            saveToCsv(results["username"], results["date"], foundAccounts)

        if config.pdf:
            saveToPdf(results["username"], results["pretty-date"], results["date"], foundAccounts)
    else:
        config.console.print("⭕ No accounts were found for the given username")