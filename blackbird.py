import argparse
import asyncio
import json

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

    parser = argparse.ArgumentParser(description='Um programa de exemplo.')
    parser.add_argument('-u', '--username', help='The target username.')
    parser.add_argument('-l', '--list-sites', action='store_true', dest='list', help='List all sites currently supported.')
    parser.add_argument('-f', '--file', help='Read results file.')
    parser.add_argument('--web', action='store_true', help='Run webserver.')
    parser.add_argument('--proxy', help='Proxy to send requests through. E.g: --proxy http://127.0.0.1:8080 ')
    parser.add_argument('--data', default='data.json', help='Location of data.json')
    parser.add_argument('-p', '--port', type=int, default=9797, help='Port for webserver')
    parser.add_argument('-o', '--output', default='results', help='Save location for user.json')
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

    blackbird = BlackBird(sites, agents, arguments.proxy, arguments.output)

    if arguments.web:
        print(f'[!] Started WebServer on http://127.0.0.1:{arguments.port}/')
        server = Webserver(blackbird)
        server.run(port=arguments.port)
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
