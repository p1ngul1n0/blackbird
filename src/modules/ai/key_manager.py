import os
import json
import requests
from pathlib import Path
from ..utils.log import logError
from ..utils.http_client import do_sync_request
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
KEY_PATH = PROJECT_ROOT / ".ai_key.json"

def fetch_api_key_from_server(config):
    try:
        headers = {
            "User-Agent": "blackbird-cli",
        }
        response = do_sync_request(
            method="GET",
            url=config.api_url + "/generate-key",
            customHeaders=headers,
            config=config,
            data=None
        )

        if response is None:
            return None

        data = response.json()

        status = data.get("status")
        success = data.get("success")
        payload = data.get("data") or {}
        message = data.get("message", "")

        if success and status == 200:
            config.console.print(f":white_check_mark: {message}")
            save_api_key_to_file(payload.get("api_key"), config)
            return True

        if status == 200 and not success:
            config.console.print(f":closed_lock_with_key: {message}")
            if payload.get("api_key"):
                save_api_key_to_file(payload["api_key"], config)
                return True

        if status == 500:
            config.console.print(f":x: {message}")
            return None

        return None
    except Exception as e:
        logError(e, "Error obtaining API Key", config)
        return None

def save_api_key_to_file(api_key, config):
    try:
        # 0o600: readable/writable by owner only, so the secret isn't world-readable
        fd = os.open(KEY_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump({"api_key": api_key}, f)
        config.console.print(f":white_check_mark: API Key saved to {KEY_PATH}")
    except Exception as e:
        config.console.print(":x: Error saving API Key to file!")
        logError(e, "Error saving API Key to file", None)

def load_api_key_from_file(config):
    if not KEY_PATH.exists():
        return None
    try:
        with open(KEY_PATH, "r") as f:
            data = json.load(f)
            if config.verbose:
                config.console.print(f":white_check_mark: API Key loaded from {KEY_PATH}")
            return data.get("api_key")
    except Exception as e:
        config.console.print(f":x: Error loading API Key {KEY_PATH}")
        logError(e, "Error loading API Key from file", None)
        return None