import requests
import config
import logging
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from log import logError

requests.packages.urllib3.disable_warnings()
proxy = config.PROXY if config.USE_PROXY == "TRUE" else None
proxies = {"http": proxy, "https": proxy} if config.USE_PROXY == "TRUE" else None

# Perform a Sync Request and return response details
def do_sync_request(method, url):
    response = requests.request(
        method=method,
        url=url,
        proxies=proxies,
        timeout=config.timeout,
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
            timeout=config.timeout,
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