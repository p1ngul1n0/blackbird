import os
import argparse
from rich.console import Console
import logging
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import config
from modules.whatsmyname.list_operations import checkUpdates
from modules.core.username import verifyUsername
from modules.core.email import verifyEmail
from modules.utils.userAgent import getRandomUserAgent
from modules.export.file_operations import createSaveDirectory
from modules.export.csv import saveToCsv
from modules.export.pdf import saveToPdf
from modules.utils.file_operations import isFile, getLinesFromFile
from modules.utils.permute import Permute
from modules.ner.entity_extraction import inialize_nlp_model
from dotenv import load_dotenv

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
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Generate a CSV with the results.",
    )
    parser.add_argument(
        "--pdf",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Generate a PDF with the results.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Show verbose output.",
    )
    parser.add_argument(
        "-ai",
        "--ai",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Extract Metadata with AI.",
    )
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
    args = parser.parse_args()

    # Store the necessary arguments to config Object
    config.username = args.username
    config.username_file = args.username_file
    config.permute = args.permute
    config.permuteall = args.permuteall
    config.csv = args.csv
    config.pdf = args.pdf
    config.filter = args.filter
    config.no_nsfw = args.no_nsfw
    config.dump = args.dump
    config.proxy = args.proxy
    config.verbose = args.verbose
    config.ai = args.ai
    config.timeout = args.timeout
    config.max_concurrent_requests = args.max_concurrent_requests
    config.email = args.email
    config.email_file = args.email_file
    config.no_update = args.no_update
    config.about = args.about
    config.instagram_session_id = os.getenv("INSTAGRAM_SESSION_ID")

    config.console = Console()

    config.dateRaw = datetime.now().strftime("%m_%d_%Y")
    config.datePretty = datetime.now().strftime("%B %d, %Y")

    config.userAgent = getRandomUserAgent(config)

    config.usernameFoundAccounts = None
    config.emailFoundAccounts = None

    config.currentUser = None
    config.currentEmail = None


def main():
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
        "           [white]Made with :beating_heart: by [red]Lucas 'P1ngul1n0' Antoniaci[/red] [/white]"
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

    if (
        not config.username
        and not config.email
        and not config.username_file
        and not config.email_file
    ):
        config.console.print("Either --username or --email is required")
        sys.exit()
    if not config.username and (config.permute or config.permuteall):
        config.console.print("Permutations requires --username")
        sys.exit()

    if config.no_update:
        config.console.print(":next_track_button:  Skipping update...")
    else:
        checkUpdates(config)

    if config.ai:
        inialize_nlp_model(config)
        config.aiModel = True

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
        for user in config.username:
            config.currentUser = user
            if config.dump or config.csv or config.pdf:
                createSaveDirectory(config)
            verifyUsername(config.currentUser, config)
            if config.csv and config.usernameFoundAccounts:
                saveToCsv(config.usernameFoundAccounts, config)
            if config.pdf and config.usernameFoundAccounts:
                saveToPdf(config.usernameFoundAccounts, "username", config)
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
        for email in config.email:
            config.currentEmail = email
            if config.dump or config.csv or config.pdf:
                createSaveDirectory(config)
            verifyEmail(email, config)
            if config.csv and config.emailFoundAccounts:
                saveToCsv(config.emailFoundAccounts, config)
            if config.pdf and config.emailFoundAccounts:
                saveToPdf(config.emailFoundAccounts, "email", config)
            config.currentEmail = None
            config.emailFoundAccounts = None

if __name__ == "__main__":
    main()
