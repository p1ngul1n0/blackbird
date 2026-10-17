import os
import argparse
import re
from rich.console import Console
import logging
import sys
from datetime import datetime
import random
import time
from rich.live import Live
from rich.text import Text

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import config
from modules.whatsmyname.list_operations import checkUpdates
from modules.core.username import verifyUsername
from modules.core.email import verifyEmail
from modules.utils.userAgent import getRandomUserAgent
from modules.export.file_operations import createSaveDirectory
from modules.export.csv import saveToCsv
from modules.export.pdf import saveToPdf
from modules.export.json import saveToJson
from modules.utils.file_operations import isFile, getLinesFromFile
from modules.utils.permute import Permute
from dotenv import load_dotenv


def sanitize_report_identifier(value: str) -> str:
    identifier = re.sub(r"[^A-Za-z0-9_-]", "_", value)
    identifier = re.sub(r"_+", "_", identifier).strip("_")
    return identifier or "report"


def generate_similar_usernames(usernames):
    variants = []
    seen = set()
    for username in usernames:
        username = username.strip()
        if not username or username in seen:
            continue
        seen.add(username)
        variants.append(username)

        if len(username) >= 3:
            prefix2 = username[:2]
            suffix2 = username[-2:]
            prefix3 = username[:3]
            suffix3 = username[-3:]

            candidates = [
                username + prefix2,
                username + suffix2,
                username + prefix3,
                username + suffix3,
                prefix2 + username,
                suffix2 + username,
                prefix3 + username,
                suffix3 + username,
                username[::-1],
                username[1:] if len(username) > 1 else username,
                username[:-1] if len(username) > 1 else username,
                username + "1",
                username + "_",
                "_" + username,
            ]
            for candidate in candidates:
                candidate = candidate.strip()
                if candidate and candidate not in seen:
                    seen.add(candidate)
                    variants.append(candidate)

    return variants

load_dotenv()


def initiate():
    if not os.path.exists("logs/"):
        os.makedirs("logs/")
    logging.basicConfig(
        filename=config.LOG_PATH,
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser(
        prog="blackbird",
        description="An OSINT tool to search for accounts by username in social networks.",
    )
    parser.add_argument(
        "-u",
        "--username",
        nargs="*",
        type=str,
        help="One or more usernames to search.",
    )
    parser.add_argument(
        "-uf",
        "--username-file",
        help="The list of usernames to be searched.",
    )
    parser.add_argument(
        "--permute",
        action="store_true",
        help="Permute usernames, ignoring single elements.",
    )
    parser.add_argument(
        "--permuteall", action="store_true", help="Permute usernames, all elements."
    )
    parser.add_argument(
        "-e",
        "--email",
        nargs="*",
        type=str,
        help="One or more email to search.",
    )
    parser.add_argument(
        "-ef",
        "--email-file",
        help="The list of emails to be searched.",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Generate a CSV with the results."
    )

    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Generate a PDF with the results."
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Generate a JSON with the results."
    )

    parser.add_argument(
        "--similar",
        action="store_true",
        help="Also search close username variants automatically."
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show verbose output."
    )

    parser.add_argument(
        "-ai", "--ai",
        action="store_true",
        help="Use AI features."
    )
    parser.add_argument("--setup-ai", action="store_true", help="Configure the API key required for AI features.")
    parser.add_argument(
        "--filter",
        help='Filter sites to be searched by list property value.E.g --filter "cat=social"',
    )
    parser.add_argument(
        "--no-nsfw", action="store_true", help="Removes NSFW sites from the search."
    )
    parser.add_argument(
        "--dump", action="store_true", help="Dump HTML content for found accounts."
    )
    parser.add_argument("--proxy", help="Proxy to send HTTP requests though.")
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout in seconds for each HTTP request (Default is 30).",
    )
    parser.add_argument(
        "--max-concurrent-requests",
        type=int,
        default=30,
        help="Specify the maximum number of concurrent requests allowed. Default is 30.",
    )
    parser.add_argument(
        "--no-update", action="store_true", help="Don't update sites lists."
    )
    parser.add_argument(
        "--about", action="store_true", help="Show about information and exit."
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show how many sites/categories are currently loaded, then exit.",
    )
    args = parser.parse_args()

    # Store the necessary arguments to config Object
    config.stats = args.stats
    config.username = args.username
    config.username_file = args.username_file
    config.permute = args.permute
    config.permuteall = args.permuteall
    config.csv = args.csv
    config.pdf = args.pdf
    config.json = args.json
    config.filter = args.filter
    config.no_nsfw = args.no_nsfw
    config.dump = args.dump
    config.proxy = args.proxy
    config.verbose = args.verbose
    config.ai = args.ai
    config.setup_ai = args.setup_ai
    config.timeout = args.timeout
    config.max_concurrent_requests = args.max_concurrent_requests
    config.email = args.email
    config.email_file = args.email_file
    config.no_update = args.no_update
    config.about = args.about
    config.similar = args.similar
    config.instagram_session_id = os.getenv("INSTAGRAM_SESSION_ID")
    config.api_url = os.getenv("API_URL")

    config.console = Console()

    # If no Instagram session ID is configured in .env, prompt for one
    # interactively — but only when this run will actually search usernames
    # (Instagram lookups don't apply to email-only searches, --about, or
    # --setup-ai), and only when stdin is a real interactive terminal.
    doing_username_search = bool(config.username or config.username_file)
    if (
        not config.instagram_session_id
        and doing_username_search
        and not config.about
        and not config.setup_ai
        and sys.stdin.isatty()
    ):
        config.console.print(
            "[bold yellow]⚠️  No INSTAGRAM_SESSION_ID found in .env[/bold yellow]"
        )
        config.console.print(
            "Enhanced Instagram metadata (obfuscated email/phone) requires a"
            " valid sessionid cookie from a logged-in Instagram session."
        )
        try:
            entered = input(
                "Paste your Instagram sessionid now (or press Enter to skip): "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            entered = ""

        if entered:
            config.instagram_session_id = entered
            config.console.print(
                "[green]✔ Using the session ID you entered for this run.[/green]"
            )
        else:
            config.console.print(
                "[yellow]Skipping enhanced Instagram metadata for this run.[/yellow]"
            )

    config.dateRaw = datetime.now().strftime("%m_%d_%Y")
    config.datePretty = datetime.now().strftime("%B %d, %Y")

    config.userAgent = getRandomUserAgent(config)

    config.usernameFoundAccounts = None
    config.emailFoundAccounts = None

    config.currentUser = None
    config.currentEmail = None

    lines = getLinesFromFile("assets/text/splash.txt")
    config.splash_line = random.choice(lines) if lines else ""


def run_interactive_menu(config):
    """Full interactive terminal app mode — launched when blackbird.py is run
    with no CLI arguments. Prompts for search type, target, and options,
    then runs the search and shows a categorized results view."""
    from rich.prompt import Prompt, Confirm

    if not sys.stdin.isatty():
        config.console.print("Either --username or --email is required")
        sys.exit()

    config.console.print("\n[bold magenta]═══ Blackbird Interactive Mode ═══[/bold magenta]\n")

    search_type = Prompt.ask(
        "[cyan]What do you want to search?[/cyan]",
        choices=["username", "email"],
        default="username",
    )

    if search_type == "username":
        raw = Prompt.ask("[cyan]Enter username(s)[/cyan] (comma-separated for multiple)")
        config.username = [u.strip() for u in raw.split(",") if u.strip()]
        if not config.username:
            config.console.print("[red]No username entered. Exiting.[/red]")
            sys.exit()

        if Confirm.ask("[cyan]Filter to a specific category or site name?[/cyan]", default=False):
            raw_filter = Prompt.ask(
                "  Enter filter (e.g. [dim]cat=social[/dim] or [dim]name=Instagram[/dim], "
                "or just type a site name like [dim]Instagram[/dim])"
            ).strip()
            if raw_filter and not re.search(r"[=~><!]", raw_filter):
                # User typed a bare word (e.g. "Instagram") — treat it as a
                # site-name filter instead of crashing on malformed syntax.
                config.filter = f"name~{raw_filter}"
            else:
                config.filter = raw_filter

        if Confirm.ask("[cyan]Save results to a PDF report when done?[/cyan]", default=True):
            config.pdf = True
        if Confirm.ask("[cyan]Also save as CSV?[/cyan]", default=False):
            config.csv = True
        if Confirm.ask(
            "[cyan]Include close username variants (like izumi, izumime, meizumi) in this search?[/cyan]",
            default=False,
        ):
            config.similar = True
        if len(config.username) > 1:
            config.currentUser = sanitize_report_identifier(
                ",".join([u.strip() for u in config.username if u.strip()])
            )
    else:
        raw = Prompt.ask("[cyan]Enter email(s)[/cyan] (comma-separated for multiple)")
        config.email = [e.strip() for e in raw.split(",") if e.strip()]
        if not config.email:
            config.console.print("[red]No email entered. Exiting.[/red]")
            sys.exit()
        if Confirm.ask("[cyan]Save results to a PDF report when done?[/cyan]", default=True):
            config.pdf = True

    config.console.print("")


def display_categorized_results(foundAccounts, config, target_label):
    """Print a results table grouped by site category (Social, Gaming, etc.),
    highlighting any extra metadata (e.g. Instagram email/phone) recovered.
    Never lets a display issue crash a search that already succeeded."""
    from rich.table import Table
    from collections import defaultdict

    if not foundAccounts:
        return

    try:
        by_category = defaultdict(list)
        for account in foundAccounts:
            category = account.get("category") or "Other"
            by_category[category].append(account)

        total = len(foundAccounts)
        config.console.print(
            f"\n[bold green]📊 Found {total} account(s) for \"{target_label}\" "
            f"across {len(by_category)} categor{'y' if len(by_category) == 1 else 'ies'}:[/bold green]\n"
        )

        table = Table(
            title=f'Blackbird Results — "{target_label}"',
            show_lines=False,
            header_style="bold white on magenta",
            title_style="bold cyan",
            expand=True,
        )
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Site", style="bold white")
        table.add_column("URL", style="bright_blue", overflow="fold")
        table.add_column("Extra Data", style="yellow")

        for category in sorted(by_category.keys(), key=lambda c: str(c)):
            accounts = sorted(by_category[category], key=lambda a: str(a.get("name", "")))
            for account in accounts:
                extra = ""
                metadata = account.get("metadata")
                if metadata:
                    parts = []
                    for item in metadata:
                        try:
                            name = str(item.get("name", "")).strip()
                            raw_value = item.get("value")
                            if isinstance(raw_value, (list, tuple, set)):
                                value = ", ".join(
                                    str(v).strip() for v in raw_value if str(v).strip()
                                )
                            elif isinstance(raw_value, dict):
                                value = ", ".join(
                                    f"{k}: {v}" for k, v in raw_value.items()
                                )
                            elif raw_value is None:
                                value = ""
                            else:
                                value = str(raw_value).strip()
                            parts.append(f"{name}: {value}" if value else name)
                        except Exception:
                            # Skip a single malformed metadata item rather than
                            # losing the whole row / whole table.
                            continue
                    extra = "\n".join(parts)
                table.add_row(
                    str(category),
                    str(account.get("name", "")),
                    str(account.get("url", "")),
                    extra,
                )

        config.console.print(table)
        config.console.print("")
    except Exception as e:
        config.console.print(
            f"[yellow]⚠️  Couldn't render the categorized results table ({e})."
            f" Your {total if 'total' in dir() else len(foundAccounts)} results were still found"
            " — use --pdf, --csv, or --json to export them.[/yellow]"
        )


if __name__ == "__main__":
    initiate()
    config.console.print(
        """[red]
    ▄▄▄▄    ██▓    ▄▄▄       ▄████▄   ██ ▄█▀ ▄▄▄▄    ██▓ ██▀███  ▓█████▄ 
    ▓█████▄ ▓██▒   ▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█████▄ ▓██▒▓██ ▒ ██▒▒██▀ ██▌
    ▒██▒ ▄██▒██░   ▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒██▒ ▄██▒██▒▓██ ░▄█ ▒░██   █▌
    ▒██░█▀  ▒██░   ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ▒██░█▀  ░██░▒██▀▀█▄  ░▓█▄   ▌
    ░▓█  ▀█▓░██████▒▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░▓█  ▀█▓░██░░██▓ ▒██▒░▒████▓ 
    ░▒▓███▀▒░ ▒░▓  ░▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░▒▓███▀▒░▓  ░ ▒▓ ░▒▓░ ▒▒▓  ▒ 
    ▒░▒   ░ ░ ░ ▒  ░ ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░▒░▒   ░  ▒ ░  ░▒ ░ ▒░ ░ ▒  ▒ 
    ░    ░   ░ ░    ░   ▒   ░        ░ ░░ ░  ░    ░  ▒ ░  ░░   ░  ░ ░  ░ 
    ░          ░  ░     ░  ░░ ░      ░  ░    ░       ░     ░        ░    
        ░                  ░                     ░               ░      

    [/red]"""
    )
    config.console.print(
        f"             [white]{config.splash_line}[/white] | by [red]Lucas Antoniaci[/red]"
    )

    if config.about:
        config.console.print(
            """
        Author: Lucas Antoniaci (p1ngul1n0)
        Description: Blackbird is an OSINT tool that perform reverse search in username and emails.
        About WhatsMyName Project: This tool search for accounts using data from the WhatsMyName project, which is an open-source tool developed by WebBreacher. WhatsMyName License: The WhatsMyName project is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0). More details (https://github.com/WebBreacher/WhatsMyName)
        """
        )
        sys.exit()

    if config.stats:
        if config.no_update:
            config.console.print(":next_track_button:  Skipping update...")
        else:
            checkUpdates(config)
        from modules.whatsmyname.list_operations import readList
        from collections import Counter

        data = readList("username", config)
        sites = data["sites"]
        cats = Counter(s["cat"] for s in sites)

        from rich.table import Table
        table = Table(title="Blackbird Site Coverage", header_style="bold white on magenta")
        table.add_column("Category", style="cyan")
        table.add_column("Sites", style="bold white", justify="right")
        for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
            table.add_row(cat, str(count))
        config.console.print(table)
        config.console.print(f"\n[bold green]Total: {len(sites)} sites across {len(cats)} categories[/bold green]")
        config.console.print(
            "[dim]This list is pulled live from the WhatsMyName project and updates automatically"
            " (unless --no-update is passed) — it's already tracking the largest actively"
            " maintained public site list, rather than a fixed bundled one.[/dim]"
        )
        sys.exit()

    if (
        not config.username
        and not config.email
        and not config.username_file
        and not config.email_file
        and not config.setup_ai
    ):
        run_interactive_menu(config)
    if not config.username and (config.permute or config.permuteall):
        config.console.print("Permutations requires --username")
        sys.exit()

    if config.no_update:
        config.console.print(":next_track_button:  Skipping update...")
    else:
        checkUpdates(config)

    if config.ai:
        config.console.print("[yellow1]:exclamation: By proceeding, you consent to share the found site names with Blackbird AI for analysis.[/yellow1] [Y/n]", end="")
        confirm = input(" > ").strip().lower()

        if confirm not in ["", "y"]:
            config.console.print(":stop_sign:  Cancelled by user.")
            sys.exit()

        from modules.ai.key_manager import load_api_key_from_file
        apikey = load_api_key_from_file(config)
        if not apikey:
            config.console.print(
                ":x: No API Key found. Please run with --setup-ai to configure the API Key."
            )
            sys.exit()

    if config.setup_ai:
        config.console.print("[yellow1]:exclamation: By continuing, you acknowledge that your IP is registered for API key management and abuse prevention.[/yellow1] [Y/n]", end="")
        confirm = input(" > ").strip().lower()

        if confirm not in ["", "y"]:
            config.console.print(":stop_sign:  Cancelled by user.")
            sys.exit()

        from modules.ai.key_manager import fetch_api_key_from_server
        result = fetch_api_key_from_server(config)
        if not result:
            config.console.print(
                ":x: Failed to fetch API Key. Please check your internet connection or try again later."
            )
        sys.exit()

    if config.username_file:
        if isFile(config.username_file):
            config.username = getLinesFromFile(config.username_file)
            config.console.print(
                f':glasses: Successfully loaded {len(config.username)} usernames from "{config.username_file}"'
            )
        else:
            config.console.print(f'❌ Could not read file "{config.username_file}"')
            sys.exit()

    if config.username:
        if (config.permute or config.permuteall) and len(config.username) > 1:
            elements = " ".join(config.username)
            way = "all" if config.permuteall else "strict"
            permute = Permute(config.username)
            config.username = permute.gather(way)
            config.console.print(
                f":glasses: Successfully loaded {len(config.username)} usernames from permuting {elements}"
            )

        original_usernames = list(config.username)
        if config.similar:
            config.username = generate_similar_usernames(config.username)
            if len(config.username) > len(original_usernames):
                config.console.print(
                    f":mag: Searching {len(config.username)} close username variants for {', '.join(original_usernames)}"
                )

        combined_accounts = []
        combined_label = ", ".join(original_usernames)
        combined_report = len(config.username) > 1 and (config.csv or config.pdf or config.json)

        if combined_report:
            config.currentUser = sanitize_report_identifier(combined_label)
            createSaveDirectory(config)

        for user in config.username:
            config.currentUser = user
            if not combined_report and (config.dump or config.csv or config.pdf or config.json):
                createSaveDirectory(config)
            verifyUsername(config.currentUser, config)
            if combined_report:
                combined_accounts.extend(config.usernameFoundAccounts or [])
            else:
                display_categorized_results(config.usernameFoundAccounts, config, config.currentUser)
                if config.ai:
                    if len(config.usernameFoundAccounts) > 2:
                        from modules.ai.client import send_prompt
                        site_names = [account.get("name", "") for account in config.usernameFoundAccounts]
                        if site_names:
                            prompt = ", ".join(site_names)

                            data = send_prompt(prompt, config)

                            if data:
                                config.ai_analysis = data
                    else:
                        config.console.print(
                            ":warning: Not enough accounts found for AI analysis. Skipping AI features."
                        )

                if config.csv and config.usernameFoundAccounts:
                    saveToCsv(config.usernameFoundAccounts, config)
                if config.pdf and config.usernameFoundAccounts:
                    saveToPdf(config.usernameFoundAccounts, "username", config)
                if config.json and config.usernameFoundAccounts:
                    saveToJson(config.usernameFoundAccounts, config)

            config.currentUser = None
            config.usernameFoundAccounts = None

        if combined_report:
            display_categorized_results(combined_accounts, config, combined_label)
            if config.csv and combined_accounts:
                saveToCsv(combined_accounts, config)
            if config.pdf and combined_accounts:
                saveToPdf(combined_accounts, "username", config)
            if config.json and combined_accounts:
                saveToJson(combined_accounts, config)
            config.currentUser = None
            config.usernameFoundAccounts = None

    if config.email_file:
        if isFile(config.email_file):
            config.email = getLinesFromFile(config.email_file)
            config.console.print(
                f':glasses: Successfully loaded {len(config.email)} emails from "{config.email_file}"'
            )
        else:
            config.console.print(f'❌ Could not read file "{config.email_file}"')
            sys.exit()

    if config.email:
        combined_accounts = []
        combined_label = ", ".join(config.email)
        combined_report = len(config.email) > 1 and (config.csv or config.pdf or config.json)

        if combined_report:
            config.currentEmail = sanitize_report_identifier(combined_label)
            createSaveDirectory(config)

        for email in config.email:
            config.currentEmail = email
            if not combined_report and (config.dump or config.csv or config.pdf or config.json):
                createSaveDirectory(config)
            verifyEmail(email, config)
            if combined_report:
                combined_accounts.extend(config.emailFoundAccounts or [])
            else:
                display_categorized_results(config.emailFoundAccounts, config, email)
                if config.ai:
                    if len(config.emailFoundAccounts) > 2:
                        from modules.ai.client import send_prompt
                        site_names = [account.get("name", "") for account in config.emailFoundAccounts]
                        if site_names:
                            prompt = ", ".join(site_names)
                        
                            data = send_prompt(prompt, config)

                            if data:
                                config.ai_analysis = data
                    else:
                        config.console.print(
                            ":warning: Not enough accounts found for AI analysis. Skipping AI features."
                        )

                if config.csv and config.emailFoundAccounts:
                    saveToCsv(config.emailFoundAccounts, config)
                if config.pdf and config.emailFoundAccounts:
                    saveToPdf(config.emailFoundAccounts, "email", config)
                if config.json and config.emailFoundAccounts:
                    saveToJson(config.emailFoundAccounts, config)
            config.currentEmail = None
            config.emailFoundAccounts = None

        if combined_report:
            display_categorized_results(combined_accounts, config, combined_label)
            if config.csv and combined_accounts:
                saveToCsv(combined_accounts, config)
            if config.pdf and combined_accounts:
                saveToPdf(combined_accounts, "email", config)
            if config.json and combined_accounts:
                saveToJson(combined_accounts, config)
            config.currentEmail = None
            config.emailFoundAccounts = None
