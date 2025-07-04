from utils.http_client import do_sync_request
import time
import sys
from rich.text import Text
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

                def type_line(line, delay=0.01):
                    text = Text.assemble(("> ", "cyan1"), (line, "default"))
                    for char in text.plain:
                        sys.stdout.write(char)
                        sys.stdout.flush()
                        time.sleep(delay)
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    time.sleep(0.05)

                def type_block(title, content_lines):
                    config.console.print(f"[[cyan1]{title}[/cyan1]]")
                    for line in content_lines:
                        type_line(f" {line}")
                    print()

                if ai_summary:
                    summary_lines = ai_summary.strip().split("\n")
                    type_block("Summary", summary_lines)

                if ai_categorization:
                    type_block("Profile Type", [ai_categorization])

                if ai_insights:
                    type_block("Insights", [f"- {insight}" for insight in ai_insights])

                if ai_risk_flags:
                    type_block("Risk Flags", [f"- {flag}" for flag in ai_risk_flags])

                if ai_tags:
                    tags_line = ", ".join(ai_tags)
                    type_block("Tags", [tags_line])

                config.console.print(f"[cyan1]:bar_chart: {remaining_quota} AI queries left for today[/]")
                return data["data"]["result"]
        return None

    except Exception as e:
        config.console.print(f":x: Error sending prompt to API!")
        logError(e, "Error sending prompt to API!", config)
        return None
