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
        "-u", "--username", nargs="*", type=str, help="The given username to search."
    )
    parser.add_argument(
        "-e", "--email", nargs="*", type=str, help="The given e-mail to search."
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
        "--no-update", action="store_true", help="Don't update sites lists."
    )
    parser.add_argument(
        "--about", action="store_true", help="Show about information and exit."
    )
    args = parser.parse_args()

    # Store the necessary arguments to config Object
    config.username = args.username
    config.csv = args.csv
    config.pdf = args.pdf
    config.filter = args.filter
    config.no_nsfw = args.no_nsfw
    config.dump = args.dump
    config.proxy = args.proxy
    config.verbose = args.verbose
    config.timeout = args.timeout
    config.email = args.email
    config.no_update = args.no_update
    config.about = args.about

    config.console = Console()

    config.dateRaw = datetime.now().strftime("%m_%d_%Y")
    config.datePretty = datetime.now().strftime("%B %d, %Y")

    config.userAgent = getRandomUserAgent()

    config.usernameFoundAccounts = None
    config.emailFoundAccounts = None

    config.currentUser = None
    config.currentEmail = None


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
        "[white]Made with :beating_heart: by Lucas Antoniaci ([red]p1ngul1n0[/red])[/white]"
    )

    if config.about:
        config.console.print(
            """
        Author: Lucas Antoniaci (p1ngul1n0)
        Description: This tool search for accounts using data from the WhatsMyName project, which is an open-source tool developed by WebBreacher.
        WhatsMyName License: The WhatsMyName project is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0).
        WhatsMyName Project: https://github.com/WebBreacher/WhatsMyName
        """
        )
        sys.exit()

    if not config.username and not config.email:
        config.console.print("Either --username or --email is required")
        sys.exit()

    if config.no_update:
        config.console.print(":next_track_button:  Skipping update...")
    else:
        checkUpdates()

    if config.username:
        for user in config.username:
            config.currentUser = user
            if config.dump or config.csv or config.pdf:
                createSaveDirectory()
            verifyUsername(config.currentUser)
            if config.csv and config.usernameFoundAccounts:
                saveToCsv(config.currentUser, config.usernameFoundAccounts)
            if config.pdf and config.usernameFoundAccounts:
                saveToPdf(config.usernameFoundAccounts, "username")
            config.currentUser = None
            config.usernameFoundAccounts = None

    if config.email:
        for email in config.email:
            config.currentEmail = email
            if config.dump or config.csv or config.pdf:
                createSaveDirectory()
            verifyEmail(config.currentEmail)
            if config.csv and config.emailFoundAccounts:
                saveToCsv(config.currentEmail, config.emailFoundAccounts)
            if config.pdf and config.emailFoundAccounts:
                saveToPdf(config.emailFoundAccounts, "email")
            config.currentEmail = None
            config.emailFoundAccounts = None
