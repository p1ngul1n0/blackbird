import sys
import os
import time
import aiohttp
import asyncio
import config
from pathlib import Path
from rich.markup import escape
import re
import hashlib


from modules.whatsmyname.list_operations import readList
from modules.utils.filter import filterFoundAccounts, filterAccounts
from modules.utils.http_client import do_async_request, do_sync_request
from modules.utils.log import logError
from modules.export.csv import saveToCsv
from modules.export.pdf import saveToPdf
from modules.export.html import dumpHTML

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
                    
                    # Save response content to a .HTML file
                    if config.dump:
                        path = os.path.join(config.saveDirectory, 'dump', f'{site["name"].replace(" ", "_")}.html')

                        result = dumpHTML(path, response["content"])
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
    data = readList()

    async with aiohttp.ClientSession() as session:
        tasks = []

        if config.filter:
            sitesToSearch = list(filter(lambda x: filterAccounts(config.filter, x), data["sites"]))
            if (len(sitesToSearch)) <= 0:
                config.console.print(f"⭕ No sites found for the given filter {config.filter}")
                sys.exit()
            else:
                config.console.print(f":page_with_curl: {len(sitesToSearch)} sites found for the given filter \"{config.filter}\"")
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
        results = {
            "results": tasksResults,
            "username": username
        }
    return results


# Start username check and presents results to user
def verifyUsername(username):
    config.console.print(
        f':play_button: Enumerating accounts with username "[cyan1]{username}[/cyan1]"'
    )
    start_time = time.time()

    # Creates directory to save PDF, CSV and HTML content
    if config.dump or config.csv or config.pdf:
        strPath = os.path.join(os.path.dirname(__file__), '..', '..', '..', Path(f"{username}_{config.dateRaw}_blackbird"))
        config.saveDirectory = strPath
        path = Path(strPath)
        if not path.exists():
            if config.verbose:
                config.console.print(escape(
        f"🆕 Creating directory to save search data [{strPath}]")
    )
            path.mkdir(parents=True, exist_ok=True)

        if config.dump:
            strPath = os.path.join(config.saveDirectory, "dump")
            path = Path(strPath)
            if not path.exists():
                if config.verbose:
                    config.console.print(escape(
                        f"🆕 Creating directory to save dump data [{escape(strPath)}]")
                    )
                path.mkdir(parents=True, exist_ok=True)

    results = asyncio.run(fetchResults(username))
    end_time = time.time()
    
    config.console.print(
        f":chequered_flag: Check completed in {round(end_time - start_time, 1)} seconds ({len(results['results'])} sites)"
    )

    if config.dump:
        config.console.print(f"💾  Dump content saved to '[cyan1]{config.username}_{config.dateRaw}_blackbird/dump[/cyan1]'")
    
    # Filter results to only found accounts
    foundAccounts = list(filter(filterFoundAccounts, results["results"]))
    
    if (len(foundAccounts) > 0):

        if config.csv:
            saveToCsv(results["username"], config.dateRaw, foundAccounts)

        if config.pdf:
            saveToPdf(results["username"], config.datePretty, config.dateRaw, foundAccounts)
    else:
        config.console.print("⭕ No accounts were found for the given username")


def verifyEmail(email):
    config.console.print(
        f':play_button: Searching e-mail "[cyan1]{email}[/cyan1]"'
    )
    # Verify e-mail in Gravatar
    email_bytes = email.encode('utf-8')
    sha256_hash = hashlib.sha256(email_bytes).hexdigest()
    response, parsedData = do_sync_request("GET", f"https://gravatar.com/{sha256_hash}.json")
    if (response.status_code == 200):
        config.console.print("✔️  E-mail found on gravatar.com")
        config.console.print(f"      Name: {parsedData['entry'][0]['displayName']}")
        config.console.print(f"      Preferred Username: {parsedData['entry'][0]['preferredUsername']}")
        config.console.print(f"      Avatar: {parsedData['entry'][0]['thumbnailUrl']}")
        config.console.print(f"      About Me: {parsedData['entry'][0]['aboutMe']}")
        config.console.print(f"      Location: {parsedData['entry'][0]['currentLocation']}")
        config.console.print(f"      Job Title: {parsedData['entry'][0]['job_title']}")
        config.console.print(f"      Company: {parsedData['entry'][0]['company']}")
        if (len(parsedData['entry'][0]['contactInfo']) > 0):
            config.console.print(f"      Contact Info:")
            for contact in parsedData['entry'][0]['contactInfo']:
                config.console.print(f"         https://{contact['value']}")
        if (len(parsedData['entry'][0]['emails']) > 0):
            config.console.print(f"      Emails:")
            for email in parsedData['entry'][0]['emails']:
                config.console.print(f"         {email['value']}")
        if (len(parsedData['entry'][0]['accounts']) > 0):
            config.console.print(f"      Accounts:")
            for account in parsedData['entry'][0]['accounts']:
                config.console.print(f"         {account['url']} [{account['name']}]")
        if (len(parsedData['entry'][0]['urls']) > 0):
            config.console.print(f"      URLs:")
            for url in parsedData['entry'][0]['urls']:
                config.console.print(f"         {url['value']}")
    else:
        config.console.print("❌  E-mail not found on gravatar.com")
    
    # Verify E-mail on Adobe.com
        headers = {"X-Ims-Clientid": "homepage_milo", "Content-Type": "application/json"}
        response, parsedData = do_sync_request("POST", f"https://auth.services.adobe.com/signin/v2/users/accounts", f"{{\"username\":\"{email}\",\"usernameType\":\"EMAIL\"}}", headers)
        if ("type" in parsedData[0]):
            config.console.print("✔️  E-mail found on adobe.com")
            config.console.print(f"      Avatar: {parsedData[0]['images']['230']}")