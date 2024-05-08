import config
from modules.utils.http_client import do_async_request, do_sync_request
from modules.whatsmyname.list_operations import readList
from src.modules.utils.input import processInput, access_json_property

def verifyEmail(email):
    config.console.print(
        f':play_button: Searching e-mail "[cyan1]{email}[/cyan1]"'
    )
    data = readList("email")
    # Verify e-mail in Gravatar
    for site in data["sites"]:
        if site["input_operation"]:
            email = processInput(config.email, site["input_operation"])
        else:
            email = config.email
        url = site["uri_check"].replace("{account}", email)
        data = site["data"].replace("{account}", email) if site["data"] else None
        headers = site["headers"] if site["headers"] else None
        response, parsedData = do_sync_request(site["method"], url, data=data, customHeaders=headers)
        if (site["e_string"] in response.text) and (
            site["e_code"] == response.status_code
        ):
            if (site["m_string"] not in response.text) and (
                site["m_code"] != response.status_code
            ):
                config.console.print(f"  ✔️  \[[cyan1]{site['name']}[/cyan1]] [bright_white]{response.url}[/bright_white]")
                if (site["metadata"]):
                    if (site["metadata"]["type"] == "JSON"):
                        for d in site["metadata"]["data"]:
                            if d["type"] == "String":
                                string = access_json_property(parsedData, d['path'])
                                config.console.print(f"         {d['name']}: {string}") if string else None
                            elif d["type"] == "Array":
                                array = access_json_property(parsedData, d['path'])
                                if (array):
                                    config.console.print(f"         {d['name']}:")
                                    for i in array:
                                        config.console.print(f"             {access_json_property(i, d['item-path'])}")
        else:
            if config.verbose:
                config.console.print(f"❌  E-mail not found [[blue]{site['name']}[/blue]]")
    
"""     # Verify E-mail on Adobe.com
        headers = {"X-Ims-Clientid": "homepage_milo", "Content-Type": "application/json"}
        response, parsedData = do_sync_request("POST", f"https://auth.services.adobe.com/signin/v2/users/accounts", f"{{\"username\":\"{email}\",\"usernameType\":\"EMAIL\"}}", headers)
        if ("type" in parsedData[0]):
            config.console.print("✔️  E-mail found on adobe.com")
            config.console.print(f"      Avatar: {parsedData[0]['images']['230']}")
        else:
            config.console.print("❌  E-mail not found on adobe.com") """