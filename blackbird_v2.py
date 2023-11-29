import requests
import hashlib
import json
import os.path


listRoute = (
    "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"
)
listName = "wmn-data.json"


def checkUpdates():
    print(f"[-] Checking for updates...")
    try:
        response = requests.get(listRoute)
        repoListHash = hashJson(response.json())

        with open(listName, "r") as openfile:
            jsonData = json.load(openfile)
            localListHash = hashJson(jsonData)

        if repoListHash == localListHash:
            print("[+] List is up to date")
        else:
            newSites = [
                x for x in response.json()["sites"] if x not in jsonData["sites"]
            ]
            print(f"[+] Updating list with {len(newSites)} new sites")
            for site in newSites:
                print(f"  |- {site['name']} [{site['cat']}]")
            downloadList()

    except Exception as err:
        print(f"[!] [FATAL] Coudn't look for updates")
        handleErr(err)


def downloadList():
    response = requests.get(listRoute)
    jsonDump = json.dumps(response.json(), indent=4)
    with open(listName, "w") as outfile:
        outfile.write(jsonDump)


def checkList():
    return os.path.isfile(listName)


def hashJson(jsonData):
    jsonDump = json.dumps(jsonData, indent=4)
    hash = hashlib.md5(jsonDump.encode("utf-8")).hexdigest()
    return hash


def handleErr(err):
    print(f"  |- An error occurred:")
    print(f"       {err}")


if __name__ == "__main__":
    if checkList():
        checkUpdates()
    else:
        downloadList()
