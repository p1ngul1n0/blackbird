import sys
import os
import time
import aiohttp
import asyncio
import config


from modules.whatsmyname.list_operations import readList
from modules.utils.parse import extractMetadata
from modules.utils.filter import filterFoundAccounts, applyFilters
from modules.utils.http_client import do_async_request
from modules.utils.log import logError
from src.modules.export.dump import dumpContent

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# Verify account existence based on list args
async def checkSite(site, method, url, session):
    returnData = {"name": site["name"], "url": url, "status": "NONE", "metadata": []}
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
                    (site["m_code"] != response["status_code"])
                    if site["m_code"] != site["e_code"]
                    else True
                ):
                    returnData["status"] = "FOUND"
                    config.console.print(
                        f"  ✔️  \[[cyan1]{site['name']}[/cyan1]] [bright_white]{response['url']}[/bright_white]"
                    )
                    if site["name"] in config.metadata_params["sites"]:
                        metadataItem = extractMetadata(
                            config.metadata_params["sites"][site["name"]],
                            response,
                            site["name"],
                        )
                        returnData["metadata"].append(metadataItem)
                    # Save response content to a .HTML file
                    if config.dump:
                        path = os.path.join(
                            config.saveDirectory, f"dump_{config.currentUser}"
                        )

                        result = dumpContent(path, site, response)
                        if result == True and config.verbose:
                            config.console.print(
                                f"      💾  Saved HTML data from found account"
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
    async with aiohttp.ClientSession() as session:
        tasks = []
        for site in config.username_sites:
            tasks.append(
                checkSite(
                    site=site,
                    method="GET",
                    url=site["uri_check"].replace("{account}", username),
                    session=session,
                )
            )
        tasksResults = await asyncio.gather(*tasks, return_exceptions=True)
        results = {"results": tasksResults, "username": username}
    return results


# Start username check and presents results to user
def verifyUsername(username):

    data = readList("username")
    config.metadata_params = readList("metadata")
    sitesToSearch = data["sites"]
    config.username_sites = applyFilters(sitesToSearch)

    config.console.print(
        f':play_button: Enumerating accounts with username "[cyan1]{username}[/cyan1]"'
    )
    start_time = time.time()
    results = asyncio.run(fetchResults(username))
    end_time = time.time()

    config.console.print(
        f":chequered_flag: Check completed in {round(end_time - start_time, 1)} seconds ({len(results['results'])} sites)"
    )

    if config.dump:
        config.console.print(
            f"💾  Dump content saved to '[cyan1]{config.currentUser}_{config.dateRaw}_blackbird/dump_{config.currentUser}[/cyan1]'"
        )

    # Filter results to only found accounts
    foundAccounts = list(filter(filterFoundAccounts, results["results"]))
    config.usernameFoundAccounts = foundAccounts

    if len(foundAccounts) <= 0:
        config.console.print("⭕ No accounts were found for the given username")

    return True
