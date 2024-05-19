import config
from lxml import etree
import re


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


def extractMetadata(metadata, response):
    metadataItem = []
    for params in metadata:
        metadataReturn = params

        if params["schema"] == "JSON":
            returnValue = access_json_property(response["json"], params["path"])
        elif params["schema"] == "HTML":
            returnValue = access_html_regex(response["content"], params["path"])
        else:
            return None

        if returnValue:
            if params["type"] == "String" and returnValue:
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

            metadataItem.append(metadataReturn)

    return metadataItem
