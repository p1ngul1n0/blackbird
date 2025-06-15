import requests
from utils.http_client import do_sync_request
import os
import json
from .key_manager import load_api_key_from_file
from utils.log import logError

def send_prompt(prompt, config):
    config.console.print(":robot: Summarizing with AI…")
    apikey = load_api_key_from_file(config)
    if not apikey:
        config.console.print(":x: No API key found. Please obtain an API key first with --setup-ai")
        return {}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "blackbird-cli",
        "x-api-key": apikey
    }
    payload = {
        "prompt": prompt
    }

    payload = json.dumps(payload)


    try:
        response = do_sync_request(
            method="POST",
            url=config.api_url + "/summarize",
            config=config,
            customHeaders=headers,
            data=payload
        )

        if response is not None:
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = None        

        if response.status_code != 200 and data:
            data = response.json()
            config.console.print(f":x: {data['message']}")
            return {}
        
        if response.status_code == 200 and data:
            return {
                "summary": data["data"]["result"],
                "remaining_quota": data["data"]["remaining_quota"]
            }

        return {}

    except Exception as e:
        config.console.print(f":x: Error sending prompt to API!")
        logError(e, "Error sending prompt to API!", config)
        return {}
