from modules.utils.http_client import do_sync_request
import config
import re
import os


def access_json_property(data, path_config):
    try:
        property_value = data
        for key in path_config:
            property_value = property_value[key]
        return property_value
    except:
        return False


def access_html_regex(data, pattern):
    try:
        match = re.search(pattern, data)
        if match:
            return match.group(1).replace("\n", "")
    except:
        return False


def download_image(metadataReturn, site):
    response = do_sync_request("GET", metadataReturn["value"])
    if config.currentUser:
        path = os.path.join(
            config.saveDirectory,
            f"images_{config.currentUser}",
            f"{site}_image.jpg",
        )
    elif config.currentEmail:
        path = os.path.join(
            config.saveDirectory,
            f"images_{config.currentEmail}",
            f"{site}_image.jpg",
        )

    if "image" in response.headers["Content-Type"]:
        with open(path, "wb") as file:
            file.write(response.content)
            metadataReturn["downloaded"] = True

    return metadataReturn


def extractMetadata(metadata, response, site):
    metadataItem = []
    for params in metadata:
        metadataReturn = params
        prefix = params["prefix"] if "prefix" in params else False

        if params["schema"] == "JSON":
            returnValue = access_json_property(response["json"], params["path"])
        elif params["schema"] == "HTML":
            returnValue = access_html_regex(response["content"], params["path"])
        else:
            return None

        if returnValue:
            if params["type"] == "String" and returnValue:
                if prefix:
                    metadataReturn["value"] = prefix + returnValue
                else:
                    metadataReturn["value"] = returnValue
                config.console.print(
                    f"      :right_arrow: {metadataReturn['name']}: {metadataReturn['value']}"
                )
            elif params["type"] == "Array" and returnValue:
                metadataReturn["value"] = []
                config.console.print(f"      :right_arrow: {metadataReturn['name']}:")
                for value in returnValue:
                    itemValue = access_json_property(value, metadataReturn["item-path"])
                    metadataReturn["value"].append(itemValue)
                    config.console.print(f"         :blue_circle: {itemValue}")
            elif params["type"] == "Image" and returnValue:
                metadataReturn["downloaded"] = False
                if prefix:
                    metadataReturn["value"] = prefix + returnValue
                else:
                    metadataReturn["value"] = returnValue
                config.console.print(
                    f"      :right_arrow: {metadataReturn['name']}: {metadataReturn['value']}"
                )
                if config.pdf:
                    metadataReturn = download_image(metadataReturn, site)

            metadataItem.append(metadataReturn)

    return metadataItem
