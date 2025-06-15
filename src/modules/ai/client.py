import requests
from utils.http_client import do_sync_request
import os
import json
from .key_manager import load_api_key_from_file
from utils.log import logError

def send_prompt(prompt, config):
    config.console.print(f":sparkles: Analyzing with AI...")
    apikey = load_api_key_from_file(config)
    if not apikey:
        config.console.print(":x: No API key found. Please obtain an API key first with --setup-ai")
        return None
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
            url=config.api_url + "/analyze",
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
            config.console.print(f":x: {data['message']}")
            return None
        
        if response.status_code == 200 and data:
            if data["success"]:
                ai_summary = data["data"]["result"]["summary"]
                ai_categorization = data["data"]["result"]["categorization"]
                ai_tags = data["data"]["result"]["tags"]
                ai_risk_flags = data["data"]["result"]["risk_flags"]
                ai_insights = data["data"]["result"]["insights"]

                remaining_quota = data["data"]["remaining_quota"]

                if ai_summary:
                    config.console.print(f":sparkles: [white]Summary:[/][cyan] \n   {ai_summary}[/]")
                if ai_categorization:
                    config.console.print(f":sparkles: [white]Categorization:[/][cyan] {ai_categorization}[/]")
                if ai_insights:
                    config.console.print(f":sparkles: [white]Insights:[/]")
                    for insight in ai_insights:
                        config.console.print(f"   [cyan] - {insight}[/]")
                if ai_risk_flags:
                    config.console.print(f":sparkles: [white]Risk Flags:[/]")
                    for risk_flag in ai_risk_flags:
                        config.console.print(f"   [cyan] - {risk_flag}[/]")
                if ai_tags:
                    config.console.print(f":sparkles: [white]Tags:[/]")
                    for tag in ai_tags:
                        config.console.print(f"   [cyan] - {tag}[/]")

                config.console.print(f"[cyan]:battery: {remaining_quota} AI queries left for today[/]")
                return data["data"]["result"]

        return None

    except Exception as e:
        config.console.print(f":x: Error sending prompt to API!")
        logError(e, "Error sending prompt to API!", config)
        return None
