import requests
import chardet


from .log import logError

requests.packages.urllib3.disable_warnings()


# Perform a Sync Request and return response details
def do_sync_request(method, url, config, data=None, customHeaders=None, cookies=None):
    headers = {"User-Agent": config.userAgent}
    if customHeaders:
        headers.update(customHeaders)
    # Only set proxies parameter if actually needed to avoid performance overhead
    request_kwargs = {
        "method": method,
        "url": url,
        "timeout": config.timeout,
        "verify": not getattr(config, "insecure", False),
        "headers": headers,
        "data": data,
        "cookies": cookies,
    }
    
    # Only add proxies parameter if a proxy is actually configured
    if config.proxy:
        request_kwargs["proxies"] = {"http": config.proxy, "https": config.proxy}
    try:
        response = requests.request(**request_kwargs)
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
    # ssl=None uses the default verifying context; ssl=False disables verification
    ssl = False if getattr(config, "insecure", False) else None
    try:
        response = await session.request(
            method,
            url,
            proxy=proxy,
            timeout=config.timeout,
            allow_redirects=True,
            ssl=ssl,
            data=data,
            headers=headers,
            max_redirects=10,
        )

        json = None
        try:
            content = await response.text()
        except (UnicodeDecodeError, LookupError):
            binaryContent = await response.read()
            encode = chardet.detect(binaryContent)["encoding"] or "utf-8"
            content = binaryContent.decode(encode, errors="replace")

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
