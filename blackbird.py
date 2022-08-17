import argparse
import asyncio
import json
from pathlib import Path
from colorama import Fore, init

from src.core import BlackBird
from src.scheme import Site
from src.service import Webserver

if __name__ == '__main__':
    init()

    print(Fore.RED + """
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

                                        Made with ❤️️ by """ + Fore.BLUE + "p1ngul1n0\n")

    parser = argparse.ArgumentParser(description='An OSINT tool to search for accounts by username in social networks.')
    parser.add_argument('-u', '--username', type=str, help='The target username.')
    parser.add_argument('-l', '--list-sites', action='store_true', dest='list', help='List all sites currently supported.')
    parser.add_argument('-f', '--file', type=str, help='Read results file.')
    parser.add_argument('--web', action='store_true', help='Run webserver.')
    parser.add_argument('--proxy', type=str, help='Proxy to send requests through. E.g: --proxy http://127.0.0.1:8080 ')
    parser.add_argument('--data', type=str, default='data.json', help='Location of data.json')
    parser.add_argument('-o', '--output', type=str, default='results', help='Save location for user.json')
    parser.add_argument('--show-all', action='store_true', help='Show all results.')
    arguments = parser.parse_args()

    # Parsing data.json to list of sites
    with open(arguments.data, 'r') as streamer:
        sites = [
            Site.parse_obj(s)
            for s in json.load(streamer)['sites']
        ]

    # Loading useragent.txt
    with open('useragents.txt', 'r') as streamer:
        agents = streamer.read().splitlines()

    blackbird = BlackBird(sites, agents, arguments.output, arguments.proxy, arguments.show_all)

    if arguments.web:
        print(f'[!] Started WebServer on http://127.0.0.1:9797/')
        server = Webserver(blackbird)
        server.run()
    elif arguments.username:
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass
        asyncio.run(blackbird.find_user_name(arguments.username))
    elif arguments.list:
        for i, site in enumerate(blackbird.get_sites(), 1):
            print(f'{i}. {site}')
    elif arguments.file:
        blackbird.read_result(arguments.file)
