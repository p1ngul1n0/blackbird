import os
from pathlib import Path
from rich.markup import escape
import time
import aiohttp
import asyncio
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from ..utils.filter import filterFoundAccounts, applyFilters
from ..utils.parse import extractMetadata
from ..utils.http_client import do_async_request
from ..whatsmyname.list_operations import readList
from ..utils.input import processInput
from ..utils.log import logError
from ..export.dump import dumpContent
from ..utils.precheck import perform_pre_check


# Verify account existence based on list args
async def checkSite(
    site,
    method,
    url,
    session,
    semaphore,
    config,
    data=None,
    headers=None,
):
    returnData = {
        "name": site["name"],
        "url": url,
        "category": site["cat"],
        "status": "NONE",
        "metadata": None,
    }
    async with semaphore:
        if site["pre_check"]:
            authenticated_headers = perform_pre_check(
                site["pre_check"], headers, config
            )
            headers = authenticated_headers
            if headers == False:
                returnData["status"] = "ERROR"
                return returnData

        response = await do_async_request(method, url, session, config, data, headers)
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
                        if site["metadata"]:
                            extractedMetadata = extractMetadata(
                                site["metadata"], response, site["name"], config
                            )
                            extractedMetadata.sort(key=lambda x: x["name"])
                            returnData["metadata"] = extractedMetadata
                        # Save response content to a .HTML file
                        if config.dump:
                            path = os.path.join(
                                config.saveDirectory, f"dump_{config.currentEmail}"
                            )

                            result = dumpContent(path, site, response, config)
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
            logError(e, f"Coudn't check {site['name']} {url}", config)
            return returnData


# Control survey on list sites
async def fetchResults(email, config):
    data = readList("email", config)
    originalEmail = email
    async with aiohttp.ClientSession() as session:
        tasks = []
        semaphore = asyncio.Semaphore(config.max_concurrent_requests)
        for site in config.email_sites:
            if site["input_operation"] != None:
                email = processInput(originalEmail, site["input_operation"], config)
            else:
                email = originalEmail
            url = site["uri_check"].replace("{account}", email)
            data = site["data"].replace("{account}", email) if site["data"] else None
            headers = site["headers"] if site["headers"] else None
            tasks.append(
                checkSite(
                    site=site,
                    method=site["method"],
                    url=url,
                    session=session,
                    semaphore=semaphore,
                    config=config,
                    data=data,
                    headers=headers,
                )
            )
        tasksResults = await asyncio.gather(*tasks, return_exceptions=True)
        results = {"results": tasksResults, "email": email}
    return results


# Start email check and presents results to user
def verifyEmail(email, config):

    data = readList("email", config)
    sitesToSearch = data["sites"]
    config.email_sites = applyFilters(sitesToSearch, config)

    config.console.print(
        f':play_button: Enumerating accounts with email "[cyan1]{email}[/cyan1]"'
    )
    start_time = time.time()
    results = asyncio.run(fetchResults(email, config))
    end_time = time.time()

    config.console.print(
        f":chequered_flag: Check completed in {round(end_time - start_time, 1)} seconds ({len(results['results'])} sites)"
    )

    if config.dump:
        config.console.print(
            f"💾  Dump content saved to '[cyan1]{config.currentEmail}_{config.dateRaw}_blackbird/dump_{config.currentEmail}[/cyan1]'"
        )

    # Filter results to only found accounts
    foundAccounts = list(filter(filterFoundAccounts, results["results"]))
    config.emailFoundAccounts = foundAccounts

    if len(foundAccounts) <= 0:
        config.console.print("⭕ No accounts were found for the given email")

    return foundAccounts
