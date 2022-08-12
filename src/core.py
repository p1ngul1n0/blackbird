import asyncio
import json
import os
import random
import time
from datetime import datetime
from typing import Dict, List, Optional

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup
from colorama import Fore

from .scheme import Report, ReportStatus, Site


class BlackBird:
    def __init__(self, sites: List[Site], agents: List[str], proxy: Optional[str], output_dir: str, show_all: bool = False):
        self.sites = sites
        self.agents = agents
        self.proxy = proxy
        self.output_dir = output_dir
        self.show_all = show_all

    async def find_user_name(self, username: str):
        start_time = time.time()
        timeout = ClientTimeout(total=10)

        print(f"{Fore.LIGHTYELLOW_EX}[!] Searching '{username}' across {len(self.sites)} social networks\033[0m")

        async with ClientSession(timeout=timeout) as session:
            tasks = [
                asyncio.ensure_future(self.make_request(session, site, username))
                for site in self.sites
            ]

            results: List[Report] = await asyncio.gather(*tasks)

            now = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
            execution_time = round(time.time() - start_time, 1)
            user_json = {
                'search-params': {
                    'username': username,
                    'sites-number': len(self.sites),
                    'date': now,
                    'execution-time': execution_time,
                },
                'sites': [r.dict(by_alias=True) for r in results]
            }
            path_save = os.path.join(self.output_dir, f'{username}.json')
            with open(path_save, 'w') as streamer:
                json.dump(user_json, streamer, indent=4, sort_keys=True)

            print(f"{Fore.LIGHTYELLOW_EX}[!] Search complete in {execution_time} seconds\033[0m")
            print(f"{Fore.LIGHTYELLOW_EX}[!] Results saved to {username}.json\033[0m")
            return user_json

    async def make_request(self, session: ClientSession, site: Site, username: str) -> Report:
        url = site.url.format(username=username)
        agent = random.choice(self.agents)
        headers = {
            'User-Agent': agent
        }

        if site.headers:
            headers.update(eval(site.headers))

        if site.json_:
            json_body = site.json_.format(username=username)
            json_body = json.loads(json_body)
        else:
            json_body = None

        try:
            async with session.request(site.method, url, json=json_body, proxy=self.proxy, headers=headers, ssl=False) as response:
                responseContent = await response.text()

                # Ready for `eval`
                if 'content-type' in response.headers and 'application/json' in response.headers["Content-Type"]:
                    jsonData = await response.json()
                else:
                    soup = BeautifulSoup(responseContent, 'html.parser')

                if eval(site.valid):
                    print(f'{Fore.LIGHTGREEN_EX}[+]\033[0m - #{site.id} {Fore.BLUE}{site.app}\033[0m {Fore.LIGHTGREEN_EX}account found\033[0m - {Fore.YELLOW}{url}\033[0m [{response.status} {response.reason}]\033[0m')

                    metadata = []
                    for d in site.metadata:
                        try:
                            value: str = eval(d.value)
                            value = value.strip('\t\r\n')
                            print(f'   |--{d.key}: {value}')
                            metadata.append({
                                'type': d.type,
                                'key': d.key,
                                'value': value
                            })
                        except Exception:
                            pass
                    return Report(
                        id=site.id, app=site.app, url=url,
                        response_status=f'{response.status} {response.reason}',
                        status=ReportStatus.FOUND,
                        metadata=metadata
                    )
                else:
                    if self.show_all:
                        print(f'[-]\033[0m - #{site.id} {Fore.BLUE}{site.app}\033[0m account not found - {Fore.YELLOW}{url}\033[0m [{response.status} {response.reason}]\033[0m')
                    return Report(
                        id=site.id, app=site.app, url=url,
                        response_status=f'{response.status} {response.reason}',
                        status=ReportStatus.NOT_FOUND,
                        metadata=[]
                    )
        except Exception as e:
            if self.show_all:
                print(f'{Fore.RED}[X]\033[0m - #{site.id} {Fore.BLUE}{site.app}\033[0m error on request ({str(e)})- {Fore.YELLOW}{url}\033[0m')
            return Report(
                id=site.id, app=site.app, url=url,
                status=ReportStatus.ERROR,
                error_message=str(e),
                metadata=[]
            )

    def get_sites(self) -> List[str]:
        return [site.app for site in self.sites]

    def read_result(self, file: str):
        try:
            with open(file, 'r') as streamer:
                result: Dict[str] = json.load(streamer)

            print(f'Loaded results file: {file}')
            print(f"Username: {result['search-params']['username']}")
            print(f"Number of sites: {result['search-params']['sites-number']}")
            print(f"Date: {result['search-params']['date']}")
            print('-------------------------------------------------')
            for report in result['sites']:
                report = Report.parse_obj(report)
                if report.status is ReportStatus.FOUND:
                    print(f'{Fore.LIGHTGREEN_EX}[+]\033[0m - {Fore.BLUE}{report.app}\033[0m {Fore.LIGHTGREEN_EX}account found\033[0m - {Fore.YELLOW}{report.url}\033[0m [{report.response_status}]\033[0m')
                    for d in report.metadata:
                        print(f"   |--{d['key']}: {d['value']}")
                elif report.status is ReportStatus.ERROR:
                    print(f'{Fore.RED}[X]\033[0m - {Fore.BLUE}{report.app}\033[0m error on request ({report.error_message}) - {Fore.YELLOW}{report.url}\033[0m')
                else:
                    print(f'{Fore.WHITE}[-]\033[0m - {Fore.BLUE}{report.app}\033[0m account not found - {Fore.YELLOW}{report.url}\033[0m [{report.response_status}]\033[0m')
        except Exception as e:
            print(f'{Fore.RED}[X] Error reading file [{str(e)}]')
