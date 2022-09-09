import json


searchDataSitesMetadataSchema = {
    "type": "object",
    "properties": {
        "key": {"type": "string"},
        "type": {"type": "string"},
        "value": {"type": "string"}
    }
}

searchDataSitesMetadataEnum = ["GET", "POST", "DELETE",
                               "PUT", "HEAD", "CONNECT", "OPTIONS", "TRACE", "PATCH"]

searchDataSitesSchema = {
    "type": "object",
    "properties": {
        "app": {"type": "string"},
        "id": {"type": "number"},
        "url": {
            "type": "string",
            "pattern": "^(https?)://"
        },
        "method": {
            "type": "string",
            "enum": searchDataSitesMetadataEnum
        },
        "valid": {"type": "string"},
        "metadata": {
            "type": "array",
            "items": searchDataSitesMetadataSchema
        }
    }
}

searchDataSchema = {
    "type": "object",
    "properties": {
        "sites": {
            "type": "array",
            "items": searchDataSitesSchema
        }
    }
}
