import time
from bs4 import BeautifulSoup
import json
import aiohttp
import asyncio
import warnings
import argparse
from colorama import init, Fore
from datetime import datetime

init()

file = open('data.json')
searchData = json.load(file)

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser(description = 'Um programa de exemplo.')
parser.add_argument('-u', action = 'store', dest = 'username',
                           required = False,
                           help = 'The target username.')
parser.add_argument('--list-sites', action = 'store_true', dest = 'list',
                           required = False,
                           help = 'List all sites currently supported.')
parser.add_argument('-r', action = 'store', dest = 'file',
                           required = False,
                           help = 'Read results file.')
arguments = parser.parse_args()

proxy = "http://127.0.0.1:8080"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0"
}

async def findUsername(username):
    start_time = time.time()
    timeout = aiohttp.ClientTimeout(total=20)
    
    print (f"{Fore.LIGHTYELLOW_EX}[!] Searching '{username}' accross {len(searchData['sites'])} social networks\033[0m")
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = []
            for u in searchData["sites"]:
                task = asyncio.ensure_future(makeRequest(session,u,username))
                tasks.append(task)

            results = await asyncio.gather(*tasks)
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            userJson = {"search-params":{"username": username, "sites-number":len(searchData['sites']),"date":now},"sites": []}
            for x in results:
                userJson["sites"].append(x)
            userFile = open(f'{username}.json','w')
            json.dump(userJson, userFile,indent=4, sort_keys=True)

            print (f"{Fore.LIGHTYELLOW_EX}[!] Search complete in {round(time.time() - start_time,1)} seconds\033[0m")
            print (f"{Fore.LIGHTYELLOW_EX}[!] Results saved to {username}.json\033[0m")

async def makeRequest(session,u,username):
    url = u["url"].format(username=username)
    jsonBody = None
    if 'headers' in u:
        headers.update(eval(u['headers']))
    if 'json' in u:
        jsonBody = u['json'].format(username=username)
        jsonBody = json.loads(jsonBody)
    async with session.request(u["method"],url,json=jsonBody, headers=headers, ssl=False) as response:
        responseContent = await response.text()
        if 'content-type' in response.headers and "application/json" in response.headers["Content-Type"]:
            jsonData = await response.json()
        else:
            soup = BeautifulSoup(responseContent, 'html.parser')
        if eval(u["valid"]):
            print (f'{Fore.LIGHTGREEN_EX}[+] - {u["app"]} account found - {url}\033[0m')
            return ({"app": u['app'], "url": url, "found": True})
        else:
            print (f'[-] - {u["app"]} account not found - {url}')
            return ({"app": u['app'], "url": url, "found": False})

def list_sites():
    i = 1
    for u in searchData["sites"]:
        print (f'{i}. {u["app"]}')
        i += 1

def read_results(file):
    try:
        f = open(file,'r')
        jsonD = json.load(f)
        print (f'Loaded results file: {file}')
        print (f"Username: {jsonD['search-params']['username']}")
        print (f"Number of sites: {jsonD['search-params']['sites-number']}")
        print (f"Date: {jsonD['search-params']['date']}")
        print ('-------------------------------------------------')
        for u in jsonD['sites']:
            if u['found'] == True:
                print (f'{Fore.LIGHTGREEN_EX}[+] - {u["app"]} account found - {u["url"]}\033[0m')
            else:
                print (f'[-] - {u["app"]} account not found - {u["url"]}')   
    except:
        print (f'{Fore.RED}[X] Could not load file!')
    
         

if arguments.username:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(findUsername(arguments.username))   
elif arguments.list:
    list_sites()
elif arguments.file:
    read_results(arguments.file)