import requests
import sys
import os
import chardet

sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from log import logError

requests.packages.urllib3.disable_warnings()


# Perform a Sync Request and return response details
def do_sync_request(method, url, config, data=None, customHeaders=None, cookies=None):
    headers = {"User-Agent": config.userAgent}
    if customHeaders:
        headers.update(customHeaders)
    proxies = {"http": config.proxy, "https": config.proxy} if config.proxy else None
    try:
        response = requests.request(
            method=method,
            url=url,
            proxies=proxies,
            timeout=config.timeout,
            verify=False,
            headers=headers,
            data=data,
            cookies=cookies,
        )
        if config.verbose:
            config.console.print(
                f"  🆗 Sync HTTP Request completed [{method} - {response.status_code}] {url}"
            )
        return response
    except Exception as e:
        if config.verbose:
            config.console.print(f"  ❌ Error in Sync HTTP Request [{method}] {url}")
        logError(e, f"Error in Sync HTTP Request [{method}] {url}", config)
        return None


# Perform an Async Request and return response details
async def do_async_request(method, url, session, config, data=None, customHeaders=None):
    headers = {"User-Agent": config.userAgent}
    if customHeaders:
        headers.update(customHeaders)
    proxy = config.proxy if config.proxy else None
    try:
        response = await session.request(
            method,
            url,
            proxy=proxy,
            timeout=config.timeout,
            allow_redirects=True,
            ssl=False,
            data=data,
            headers=headers,
            max_redirects=10,
        )

        json = None
        try:
            content = await response.text()
        except:
            binaryContent = await response.read()
            encode = chardet.detect(binaryContent)["encoding"]
            content = binaryContent.decode(encode)

        if "Content-Type" in response.headers:
            if "application/json" in response.headers["Content-Type"]:
                json = await response.json()

        responseData = {
            "url": url,
            "status_code": response.status,
            "headers": response.headers,
            "content": content,
            "json": json,
        }

        if config.verbose:
            config.console.print(
                f"  🆗 Async HTTP Request completed [{method} - {response.status}] {url}"
            )
        return responseData
    except Exception as e:
        if config.verbose:
            config.console.print(f"  ❌ Error in Async HTTP Request [{method}] {url}")
        logError(e, f"Error in Async HTTP Request [{method}] {url}", config)
        return None
