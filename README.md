<img alt="blackbird-logo" align="left" width="300" height="300" src="https://raw.githubusercontent.com/p1ngul1n0/badges/main/badges/22.png">
<h1>Blackbird</h1>

### A versatile OSINT tool for quickly searching user accounts by username or email across numerous platforms, aiding comprehensive digital investigations.
> The Lockheed SR-71 "Blackbird" is a long-range, high-altitude, Mach 3+ strategic reconnaissance aircraft developed and manufactured by the American aerospace company Lockheed Corporation.

</br>

<img alt="blackbird-cli" align="center" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_printscreen.png">

## Setup

#### Clone the repository
```shell
git clone https://github.com/p1ngul1n0/blackbird
cd blackbird
```

#### Install requirements
```shell
pip install -r requirements.txt
```

## Usage

#### Search by username
```python
python blackbird.py --username username1 username2 username3
```

#### Search by email
```python
python blackbird.py --email email1@email email2@email email3@email
```

#### Export to PDF
```python
python blackbird.py --username username1 --pdf
```
<img alt="blackbird-pdf-cover" width="300" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/blackbird_report_pdf_results.png">

#### Export to CSV
```python
python blackbird.py --username username1 --csv
```

#### DUMP
Dump all found account HTTP responses.
```python
python blackbird.py --username username1 --dump
```

#### All of the above
The previous arguments can all be used together in one single command.
```python
python blackbird.py --username username1 username2 username3 --email email1@email email2@email email3@email --pdf --csv --dump
```

#### Other
```
usage: blackbird [-h] [-u [USERNAME ...]] [-e [EMAIL ...]] [--csv | --no-csv] [--pdf | --no-pdf] [-v | --verbose | --no-verbose] [--filter FILTER] [--no-nsfw] [--dump]
                 [--proxy PROXY] [--timeout TIMEOUT] [--no-update] [--about]

An OSINT tool to search for accounts by username in social networks.

options:
  -h, --help            show this help message and exit
  -u [USERNAME ...], --username [USERNAME ...]
                        One or more usernames to search.
  -e [EMAIL ...], --email [EMAIL ...]
                        One or more email to search.
  --csv, --no-csv       Generate a CSV with the results.
  --pdf, --no-pdf       Generate a PDF with the results.
  -v, --verbose, --no-verbose
                        Show verbose output.
  --filter FILTER       Filter sites to be searched by list property value.E.g --filter "cat=social"
  --no-nsfw             Removes NSFW sites from the search.
  --dump                Dump HTML content for found accounts.
  --proxy PROXY         Proxy to send HTTP requests through.
  --timeout TIMEOUT     Timeout in seconds for each HTTP request (Default is 30).
  --no-update           Don't update sites lists.
  --about               Show about information and exit.
```

## WhatsMyName Integration
#### Blackbird is fully integrated with <a href="https://github.com/WebBreacher/WhatsMyName">WhatsMyName</a> project,  witch has 600+ sites to perform accurate reverse username search.

## Sponsors
This project is proudly sponsored by:

[<img alt="Cyber Hunter Lab Logo" align="center" width="20%" src="https://raw.githubusercontent.com/p1ngul1n0/src/master/logo_chl.jpg" />](https://site.cyberhunteracademy.com/)

## Disclaimer
```
This or previous program is for Educational purpose ONLY. Do not use it without permission. 
The usual disclaimer applies, especially the fact that me (P1ngul1n0) is not liable for any 
damages caused by direct or indirect use of the information or functionality provided by these 
programs. The author or any Internet provider bears NO responsibility for content or misuse 
of these programs or any derivatives thereof. By using these programs you accept the fact 
that any damage (dataloss, system crash, system compromise, etc.) caused by the use of these 
programs is not P1ngul1n0's responsibility.
```


## Contributors 🏅
<a href="https://github.com/p1ngul1n0/blackbird/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=p1ngul1n0/blackbird" />
</a>

I'm grateful to all contributors who improved and bugfixed the project.

- <a href="https://github.com/RelatedTitle">@RelatedTitle</a> - Fixed the Youtube user search URL.
- <a href="https://github.com/prisar">@prisar</a> - Fixed the OS check for AsyncIO policy.
- <a href="https://github.com/itmaru">@itmaru</a> - Fixed 'across' typo.
- <a href="https://github.com/Bryan-Herrera-DEV">@Bryan-Herrera-DEV</a> - Added Universocraft site.
- <a href="https://github.com/devXprite">@devXprite</a> - Added NPM and PyPI sites.
- <a href="https://github.com/ChrisCarini">@ChrisCarini</a> - Fixed 'supported' typo.
- <a href="https://github.com/Pandede">@Pandede</a> - Fixed <a href="https://github.com/p1ngul1n0/blackbird/issues/24">No such file or directory: 'python' #24 </a> issue, reformatted with autopep8, implemented `enumerate` and code splitting for functions.
- <a href="https://github.com/tr33n">@tr33n</a> - Implemented random UserAgent for each request.
- <a href="https://github.com/Sebsebzen">@Sebsebzen</a> - Added VKontakte (with metadata).
- <a href="https://github.com/LsvanDarko">@LsvanDarko</a> - Added requests package to requirements.txt.
- <a href="https://github.com/wymiotkloaki">@wymiotkloaki</a> - Added basic .gitignore file and 21 sites.
- <a href="https://github.com/dwaltsch">@dwaltsch</a> - Added Dockerfile.
- <a href="https://github.com/yutodadil">@yutodadil</a> - Added Zepeto and increased timeout to 10 seconds.
- <a href="https://github.com/Pitastic">@pitastic</a> - Fixed <a href="https://github.com/p1ngul1n0/blackbird/issues/42">Access to 127.0.0.1 was denied #42 </a> issue.
- <a href="https://github.com/qqux">@qqux</a> - Added 6 sites (YouPic, VIEWBUG, Art Limited, 35photo.pro, Purple Port, Pixieset).

## Contact
Feel free to contact me at <a href="https://x.com/p1ngul1n0">X</a>
