import requests
from bs4 import BeautifulSoup
import json
import warnings
import argparse

warnings.filterwarnings('ignore')
parser = argparse.ArgumentParser(description = 'Um programa de exemplo.')
parser.add_argument('-u', action = 'store', dest = 'username',
                           required = True,
                           help = 'The target username.')
arguments = parser.parse_args()
proxy = {
    "http": "http://127.0.0.1:8080",
    "https":"http://127.0.0.1:8080"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0"
}

def findUsername(username):
    urls = [
        {"app": "Facebook","url":f'https://www.facebook.com/{username}', "valid": "response.status_code == 200"},
        {"app": "YouTube","url":f'https://www.youtube.com/user/{username}/videos', "valid": "response.status_code == 200"},
        {"app": "Twitter","url":f'https://nitter.net/{username}', "valid": "response.status_code == 200"},
        {"app": "Telegram","url":f'https://t.me/{username}', "valid": "len(soup.find_all('img', class_='tgme_page_photo_image'))  > 0"},
        {"app": "TikTok","url":f'https://www.tiktok.com/@{username}', "valid": "response.status_code == 200"},
        {"app": "Tinder","url":f'https://tinder.com/@{username}', "valid": "'@' in soup.find('meta', property='og:title')['content']"},
        {"app": "Instagram","url":f'https://www.picuki.com/profile/{username}', "valid": "response.status_code == 200"},
        {"app": "Pinterest","url":f'https://pinterest.com/{username}/', "valid": "response.status_code == 200"},
        {"app": "Snapchat","url":f'https://feelinsonice.appspot.com/web/deeplink/snapcode?username={username}&size=400&type=SVG', "valid": "soup.find('defs') != None"},
        {"app": "Reddit","url":f'https://www.reddit.com/user/{username}/about.json', "valid": "response.status_code == 200"},
        {"app": "Soundcloud","url":f'https://soundcloud.com/{username}', "valid": "response.status_code == 200"},
        {"app": "Github","url":f'https://github.com/{username}', "valid": "response.status_code == 200"},
        {"app": "Steam","url":f'https://steamcommunity.com/id/{username}/', "valid": "'Error' not in soup.find('title').string"},
        {"app": "Linktree","url":f'https://linktr.ee/{username}', "valid": "response.status_code == 200"},
        {"app": "Xbox Gamertag","url":f'https://www.xboxgamertag.com/search/{username}', "valid": "response.status_code == 200"},
        {"app": "Twitter Archived","url":f'http://archive.org/wayback/available?url=https://twitter.com/{username}', "valid": "'available' in response.text"},
        {"app": "Xvideos","url":f'https://www.xvideos.com/profiles/{username}', "valid": "response.status_code == 200"},
        {"app": "PornHub","url":f'https://www.pornhub.com/users/{username}', "valid": "response.status_code == 200"},
        {"app": "Xhamster","url":f'https://xhamster.com/users/{username}', "valid": "response.status_code == 200"},
        {"app": "Periscope","url":f'https://www.periscope.tv/{username}', "valid": "response.status_code == 200"},
        {"app": "Ask FM","url":f'https://ask.fm/{username}', "valid": "response.status_code == 200"},
        {"app": "Vimeo","url":f'https://vimeo.com/{username}', "valid": "response.status_code == 200"},
        {"app": "Twitch","url":f'https://www.twitch.tv/{username}', "valid": "' - ' in soup.find('meta', property='og:title')['content']"},
        {"app": "Pastebin","url":f'https://pastebin.com/u/{username}', "valid": "response.status_code == 200"},
        {"app": "WordPress","url":f'https://profiles.wordpress.org/{username}/', "valid": "response.status_code == 200"},
        {"app": "AllMyLinks","url":f'https://allmylinks.com/{username}', "valid": "response.status_code == 200"},
        {"app": "Buzzfeed","url":f'https://www.buzzfeed.com/{username}', "valid": "response.status_code == 200"},
        {"app": "JsFiddle","url":f'https://jsfiddle.net/user/{username}/', "valid": "response.status_code == 200"},
        {"app": "Sourceforge","url":f'https://sourceforge.net/u/{username}/profile', "valid": "response.status_code == 200"},
        {"app": "Kickstarter","url":f'https://www.kickstarter.com/profile/{username}', "valid": "response.status_code == 200"},
        {"app": "Smule","url":f'https://www.smule.com/{username}', "valid": "'404' not in soup.find('title').string"},
        {"app": "Blogspot","url":f'http://{username}.blogspot.com/', "valid": "response.status_code == 200"},
        {"app": "Tradingview","url":f'https://www.tradingview.com/u/{username}/', "valid": "response.status_code == 200"},
        {"app": "Internet Archive","url":f'https://archive.org/details/@{username}', "valid": "'cannot find account' not in soup.find('title').string"},
        {"app": "Alura","url":f'https://cursos.alura.com.br/user/{username}', "valid": "response.status_code == 200"},
        {"app": "Behance","url":f'https://www.behance.net/{username}/moodboards', "valid": "response.status_code == 200"},
        {"app": "MySpace","url":f'https://myspace.com/{username}', "valid": "response.status_code == 200"},
        {"app": "Disqus","url":f'https://disqus.com/by/{username}/', "valid": "response.status_code == 200"},
        {"app": "Slideshare","url":f'https://www.slideshare.net/{username}', "valid": "response.status_code == 200"},
        {"app": "Rumble","url":f'https://rumble.com/user/{username}', "valid": "response.status_code == 200"},
        {"app": "TripAdvisor","url":f'https://www.tripadvisor.com/Profile/{username}', "valid": "response.status_code == 200"},
        {"app": "Ebay","url":f'https://www.ebay.com/usr/{username}', "valid": "'error' not in soup.find('title').string"},
    ]

    print (f"Searching '{username}' accross {len(urls)} social networks")
    for u in urls:
        response = requests.get(u["url"], headers=headers, verify=False)
        if 'content-type' in response.headers and response.headers["Content-Type"] == "application/json":
            jsonData = json.loads(response.content)
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
        if eval(u["valid"]):
            print (f'\033[92m[+] - {u["app"]} account found - {u["url"]}\033[0m')
        else:
            print (f'[-] - {u["app"]} account not found - {u["url"]}')

findUsername(arguments.username)
